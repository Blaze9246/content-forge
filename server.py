#!/usr/bin/env python3
"""
Blaze Content Forge - Combined Server
Serves both frontend and backend API
"""

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os

# Import Content Forge
from backend.blaze_content_forge import ContentForge, BrandProfile

app = Flask(__name__, static_folder='frontend')
CORS(app)

# Initialize Content Forge
forge = ContentForge()

# Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

# API Routes
@app.route('/industries', methods=['GET'])
def get_industries():
    industries = list(forge.HOOKS.keys())
    return jsonify({"industries": industries})

@app.route('/brands', methods=['GET'])
def get_brands():
    brands = [{
        "name": "Default Brand",
        "industry": "ecommerce",
        "voice": "friendly",
        "target_audience": "Millennials and Gen Z shoppers",
        "content_pillars": ["product_features", "customer_stories", "tips_tricks", "behind_scenes"]
    }]
    return jsonify({"brands": brands})

@app.route('/generate/carousel', methods=['POST'])
def generate_carousel():
    try:
        data = request.get_json()
        
        topic = data.get('topic', 'Marketing Tips')
        industry = data.get('industry', 'ecommerce')
        brand_voice = data.get('brand_voice', 'friendly')
        num_slides = int(data.get('num_slides', 7))
        template = data.get('template', 'tips')
        
        content = forge.generate_carousel_post(
            topic=topic,
            industry=industry,
            num_slides=num_slides,
            brand_voice=brand_voice,
            template_type=template
        )
        
        result = {
            "content_type": content.content_type,
            "title": content.title,
            "slides": content.slides,
            "caption": content.caption,
            "hashtags": content.hashtags,
            "hook": content.hook,
            "cta": content.cta,
            "engagement_score": content.engagement_score,
            "best_posting_time": content.best_posting_time,
            "brand_voice": content.brand_voice
        }
        
        return jsonify({"success": True, "content": result})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/generate/caption', methods=['POST'])
def generate_caption():
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        industry = data.get('industry', 'ecommerce')
        
        caption = forge.generate_caption(topic, industry)
        hashtags = forge.generate_hashtags(topic, industry)
        
        return jsonify({
            "success": True,
            "caption": caption,
            "hashtags": hashtags
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/generate/hashtags', methods=['POST'])
def generate_hashtags_route():
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        industry = data.get('industry', 'ecommerce')
        num_sets = int(data.get('num_sets', 3))
        
        hashtag_sets = []
        for i in range(num_sets):
            tags = forge.generate_hashtags(topic, industry)
            hashtag_sets.append({
                "set_number": i + 1,
                "hashtags": tags,
                "count": len(tags)
            })
        
        return jsonify({"success": True, "hashtag_sets": hashtag_sets})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/generate/calendar', methods=['POST'])
def generate_calendar():
    try:
        data = request.get_json()
        brand_name = data.get('brand_name', 'Brand')
        industry = data.get('industry', 'ecommerce')
        weeks = int(data.get('weeks', 2))
        posts_per_week = int(data.get('posts_per_week', 3))
        
        brand = BrandProfile(
            name=brand_name,
            industry=industry,
            voice='friendly',
            target_audience='General audience',
            color_scheme=['#000000', '#FFFFFF'],
            content_pillars=['tips', 'products', 'stories', 'behind_scenes'],
            posting_frequency=posts_per_week
        )
        
        calendar = forge.generate_content_calendar(brand, weeks)
        
        return jsonify({"success": True, "calendar": calendar})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
