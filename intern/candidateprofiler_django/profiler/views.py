from django.shortcuts import render
from .resume_parser import extract_resume_data
from .firecrawl_api import firecrawl_search
from .similarity import fuzzy_match, jaccard_sim
from .utils.face_match import match_image_and_extract_text


def home(request):
    return render(request, 'profiler/home.html')


def match_profiles(request):
    name = request.GET.get("name", "")
    email = request.GET.get("email", "")
    github = request.GET.get("github", "")
    linkedin = request.GET.get("linkedin", "")
    user_image = request.FILES.get("image")

    platforms = [
        "site:linkedin.com",
        "site:github.com",
        "site:medium.com",
        "site:instagram.com",
    ]

    results = []

    for platform in platforms:
        query = f"{name} {email} {platform}"
        fc_result = firecrawl_search(query)
        links = fc_result.get("links", [])

        for link in links:
            title = link.get("title", "")
            url = link.get("url", "")
            image_url = link.get("image", "")  # Optional image from Firecrawl

            score_fuzzy = fuzzy_match(title, name)
            score_jaccard = jaccard_sim(title, name)

            # Face + OCR
            image_score = 0.0
            ocr_text = ""
            if user_image and image_url:
                try:
                    match = match_image_and_extract_text(user_image, image_url)
                    image_score = match.get("similarity_score", 0)
                    ocr_text = match.get("ocr_text", "")
                except Exception as e:
                    print(f"[Image Match Error] {e}")

            # Simulated activity score (you can later base this on actual scraping, e.g., number of posts or stars)
            activity_score = 10 if platform in ["site:github.com", "site:linkedin.com"] else 5

            # Final confidence score
            confidence = (
                (score_fuzzy * 0.20) +
                (image_score * 0.40) +
                (score_jaccard * 0.30) +
                (activity_score * 1.0)  # out of 10, no conversion needed
            )

            results.append({
                "platform": platform.replace("site:", ""),
                "title": title,
                "url": url,
                "fuzzy_score": score_fuzzy,
                "jaccard_score": round(score_jaccard, 2),
                "image_score": image_score,
                "ocr_text": ocr_text,
                "confidence": round(confidence, 2)
            })

    return render(request, "profiler/match_results.html", {"results": results})

from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
from .models import MatchResult


def download_pdf(request):
    results = MatchResult.objects.order_by('-created_at')[:10]  # latest
    html = render_to_string("profiler/pdf_report.html", {"results": results, "name": results[0].name if results else "Candidate"})
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error rendering PDF", status=400)
    return response
