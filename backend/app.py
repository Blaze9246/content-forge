#!/usr/bin/env python3
"""
Blaze Content Forge - Web API
Flask backend for Content Forge web app
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Import ContentForge from same directory
from blaze_content_forge import ContentForge, BrandProfile, ContentPiece

app = Flask(__name__)
CORS(app)

# Initialize Content Forge
forge = ContentForge()


@app.route('/')
def home():
    return jsonify({
        "message": "🎨 Blaze Content Forge API",
        "status": "running",
        "endpoints": {
            "POST /generate/carousel": "Generate carousel post",
            "POST /generate/caption": "Generate caption only",
            "POST /generate/hashtags": "Generate hashtag sets",
            "POST /generate/calendar": "Generate content calendar",
            "GET /brands": "List available brand profiles",
            "GET /industries": "List supported industries"
        }
    })


@app.route('/brands', methods=['GET'])
def get_brands():
    """Get list of pre-configured brand profiles"""
    brands = [
        {
            "name": "Default Brand",
            "industry": "ecommerce",
            "voice": "friendly",
            "target_audience": "Millennials and Gen Z shoppers",
            "content_pillars": ["product_features", "customer_stories", "tips_tricks", "behind_scenes"]
        }
    ]
    return jsonify({"brands": brands})


@app.route('/industries', methods=['GET'])
def get_industries():
    """Get supported industries"""
    industries = list(forge.HOOKS.keys())
    return jsonify({"industries": industries})


@app.route('/generate/carousel', methods=['POST'])
def generate_carousel():
    """
    Generate Instagram carousel post
    
    Body:
    {
        "topic": "Email Marketing Tips",
        "industry": "ecommerce",
        "brand_voice": "friendly",
        "num_slides": 7,
        "template": "tips"  // 'tips', 'mistakes', 'steps', 'guide'
    }
    """
    try:
        data = request.get_json()
        
        topic = data.get('topic', 'Marketing Tips')
        industry = data.get('industry', 'ecommerce')
        brand_voice = data.get('brand_voice', 'friendly')
        num_slides = int(data.get('num_slides', 7))
        template = data.get('template', 'tips')
        
        # Generate carousel
        content = forge.generate_carousel_post(
            topic=topic,
            industry=industry,
            num_slides=num_slides,
            brand_voice=brand_voice,
            template_type=template
        )
        
        # Convert to dict
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
    """Generate caption only"""
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
def generate_hashtags():
    """Generate hashtag sets"""
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
    """Generate content calendar"""
    try:
        data = request.get_json()
        brand_name = data.get('brand_name', 'Brand')
        industry = data.get('industry', 'ecommerce')
        weeks = int(data.get('weeks', 2))
        posts_per_week = int(data.get('posts_per_week', 3))
        
        # Create brand profile
        brand = BrandProfile(
            name=brand_name,
            industry=industry,
            voice='friendly',
            target_audience='General audience',
            color_scheme=['#000000', '#FFFFFF'],
            content_pillars=['tips', 'products', 'stories', 'behind_scenes'],
            posting_frequency=posts_per_week
        )
        
        # Generate calendar
        calendar = forge.generate_content_calendar(brand, weeks)
        
        return jsonify({"success": True, "calendar": calendar})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
