from flask import Flask, render_template, request
from urllib.parse import urlparse
import re

app = Flask(__name__)

SUPPORTED_PLATFORMS = {
    "youtube": [
        "youtube.com",
        "youtu.be"
    ],
    "tiktok": [
        "tiktok.com"
    ],
    "instagram": [
        "instagram.com"
    ],
    "facebook": [
        "facebook.com",
        "fb.watch"
    ],
    "x": [
        "twitter.com",
        "x.com"
    ],
    "pinterest": [
        "pinterest.com",
        "pin.it"
    ]
}


def detect_platform(url):
    try:
        hostname = urlparse(url).netloc.lower()
        hostname = hostname.replace("www.", "")

        for platform, domains in SUPPORTED_PLATFORMS.items():
            for domain in domains:
                if hostname == domain or hostname.endswith("." + domain):
                    return platform

    except Exception:
        pass

    return None


def valid_url(url):
    pattern = r"^https?://.+"
    return bool(re.match(pattern, url.strip(), re.IGNORECASE))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url", "").strip()

    if not url:
        return render_template(
            "result.html",
            error="يرجى إدخال رابط الفيديو."
        )

    if not valid_url(url):
        return render_template(
            "result.html",
            error="الرابط غير صحيح. يجب أن يبدأ بـ http:// أو https://"
        )

    platform = detect_platform(url)

    if not platform:
        return render_template(
            "result.html",
            error="هذه المنصة غير مدعومة حاليًا."
        )

    platform_names = {
        "youtube": "YouTube",
        "tiktok": "TikTok",
        "instagram": "Instagram",
        "facebook": "Facebook",
        "x": "X / Twitter",
        "pinterest": "Pinterest"
    }

    return render_template(
        "result.html",
        platform=platform_names.get(platform, platform),
        url=url
    )


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "result.html",
        error="الصفحة غير موجودة."
    ), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
