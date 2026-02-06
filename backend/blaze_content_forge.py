#!/usr/bin/env python3
"""
🎨 BLAZE CONTENT FORGE
AI-Powered Instagram Content Generator for Multi-Brand Management

Creates carousel posts, captions, and hashtag sets automatically.
Perfect for managing content across multiple client brands.

Features:
- Carousel post generator (5-10 slides)
- Caption writing with hooks
- Hashtag research and optimization
- Content calendar planning
- Brand voice customization
- Engagement prediction
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ContentPiece:
    """A single piece of content"""
    content_type: str  # 'carousel', 'single', 'reel', 'story'
    title: str
    slides: List[Dict]  # For carousels
    caption: str
    hashtags: List[str]
    hook: str
    cta: str
    engagement_score: int
    best_posting_time: str
    brand_voice: str


@dataclass
class BrandProfile:
    """Brand configuration"""
    name: str
    industry: str
    voice: str  # 'professional', 'playful', 'luxury', 'edgy', 'friendly'
    target_audience: str
    color_scheme: List[str]
    content_pillars: List[str]
    posting_frequency: int  # posts per week


class ContentForge:
    """
    AI-powered content generation engine
    Creates Instagram content that converts
    """
    
    # Hook templates by industry
    HOOKS = {
        'ecommerce': [
            "Stop scrolling if you want to {benefit} 🔥",
            "The {product} that changed everything for me...",
            "POV: You finally found {solution}",
            "3 {things} I wish I knew before {action}",
            "Unpopular opinion: {opinion} 👇",
            "Save this if you're struggling with {problem}",
            "This {product} went viral for a reason...",
            "The truth about {topic} nobody talks about",
            "Wait for the transformation... 😱",
            "Which one are you choosing? {options}",
        ],
        'saas': [
            "The {tool} that saved me {time} every week",
            "Stop doing {task} manually (do this instead)",
            "If you're not using {tool}, you're working too hard",
            "This automation changed my business forever",
            "The $0 → ${amount} journey (thread) 🧵",
            "Bookmark this for your next {project}",
            "Free tools that work better than paid ones:",
            "The workflow that 10x'd my productivity",
        ],
        'fitness': [
            "The only {exercise} you need for {goal}",
            "3 months ago vs now 💪",
            "Stop making these {number} mistakes...",
            "Your {body_part} will thank you for this",
            "The {number} minute workout that actually works",
            "Transformation Tuesday hits different when...",
            "This changed my relationship with {topic}",
        ],
        'food': [
            "The {number} ingredient {dish} everyone needs",
            "POV: You finally mastered {recipe}",
            "Stop ordering takeout and make this instead 👨‍🍳",
            "This {dish} recipe broke the internet...",
            "Meal prep Sunday just got easier",
            "The secret ingredient you never knew you needed",
            "Restaurant-quality {dish} at home 🏠",
        ],
        'fashion': [
            "The {item} that goes with EVERYTHING",
            "How to style {item} {number} ways",
            "This outfit cost less than your coffee ☕",
            "The trend I'm taking into {season}",
            "Capsule wardrobe essentials you actually need",
            "From desk to dinner in one outfit ✨",
            "The color combination nobody saw coming",
        ],
        'general': [
            "The {number} things I learned from {experience}",
            "Unpopular opinion that might help you: 👇",
            "If you're reading this, it's a sign to {action}",
            "The {topic} guide I wish I had sooner",
            "Stop scrolling and {action} 🔥",
            "This mindset shift changed everything",
            "Bookmark this for when you need it 📌",
        ]
    }
    
    # Carousel slide templates
    CAROUSEL_TEMPLATES = {
        'tips': {
            'structure': ['hook', 'intro', 'tip_1', 'tip_2', 'tip_3', 'bonus', 'cta'],
            'titles': [
                "{number} {topic} Tips That Actually Work",
                "Save These {topic} Hacks 📌",
                "The {topic} Guide You Need",
            ]
        },
        'mistakes': {
            'structure': ['hook', 'intro', 'mistake_1', 'mistake_2', 'mistake_3', 'solution', 'cta'],
            'titles': [
                "Stop Making These {topic} Mistakes 🚫",
                "{number} Things Ruining Your {topic}",
                "Mistakes Costing You {cost}",
            ]
        },
        'steps': {
            'structure': ['hook', 'intro', 'step_1', 'step_2', 'step_3', 'step_4', 'result', 'cta'],
            'titles': [
                "How to {goal} in {number} Steps",
                "The {topic} Blueprint 🗺️",
                "From {start} to {end} (Step-by-Step)",
            ]
        },
        'mistakes_to_success': {
            'structure': ['hook', 'pain_point', 'mistake_1', 'mistake_2', 'solution', 'results', 'cta'],
            'titles': [
                "How I Fixed My {problem}",
                "I Was {action} Wrong for Years 😅",
                "The {topic} Glow-Up Strategy",
            ]
        }
    }
    
    # CTA templates
    CTAS = [
        "Save this for later 📌",
        "Drop a 🔥 if you agree",
        "Which one will you try first? 👇",
        "Share this with someone who needs to see it",
        "Comment '{keyword}' for the full guide",
        "Link in bio for more 👆",
        "Follow for daily {topic} tips",
        "Tag someone who's struggling with {problem}",
        "Double tap if this helped you ❤️",
        "What's your biggest {topic} challenge? Tell me below 👇",
    ]
    
    # Hashtag banks by category
    HASHTAGS = {
        'ecommerce': ['#ecommerce', '#shopify', '#onlineshop', '#smallbusiness', '#entrepreneur', 
                      '#digitalmarketing', '#onlinestore', '#dropshipping', '#ecommercebusiness', '#marketing'],
        'saas': ['#saas', '#startup', '#tech', '#software', '#b2b', '#growthhacking', '#productivity', 
                 '#automation', '#businesstools', '#entrepreneurship'],
        'fitness': ['#fitness', '#workout', '#health', '#gym', '#wellness', '#fitnessmotivation', 
                    '#healthylifestyle', '#training', '#fitnessjourney', '#strong'],
        'food': ['#foodie', '#foodblogger', '#recipe', '#homemade', '#cooking', '#foodphotography', 
                 '#instafood', '#healthyfood', '#foodstagram', '#yummy'],
        'fashion': ['#fashion', '#style', '#ootd', '#outfit', '#fashionblogger', '#streetstyle', 
                    '#instafashion', '#fashionista', '#styleinspo', '#lookbook'],
        'marketing': ['#marketing', '#digitalmarketing', '#socialmedia', '#branding', '#contentmarketing',
                      '#marketingtips', '#growth', '#socialmediamarketing', '#marketingstrategy', '#seo'],
        'general': ['#instagood', '#photooftheday', '#love', '#instadaily', '#follow', '#like', 
                    '#picoftheday', '#beautiful', '#happy', '#life']
    }
    
    def __init__(self):
        self.brands = {}
        self.content_history = []
    
    def create_brand(self, name: str, industry: str, voice: str, 
                     target_audience: str, content_pillars: List[str],
                     posting_frequency: int = 5) -> BrandProfile:
        """Create a new brand profile"""
        brand = BrandProfile(
            name=name,
            industry=industry,
            voice=voice,
            target_audience=target_audience,
            color_scheme=self._generate_colors(),
            content_pillars=content_pillars,
            posting_frequency=posting_frequency
        )
        self.brands[name] = brand
        return brand
    
    def _generate_colors(self) -> List[str]:
        """Generate a cohesive color scheme"""
        palettes = [
            ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            ['#6C5CE7', '#A29BFE', '#74B9FF', '#0984E3', '#00B894'],
            ['#FD79A8', '#FDCB6E', '#6C5CE7', '#00B894', '#E17055'],
            ['#2D3436', '#636E72', '#B2BEC3', '#DFE6E9', '#00B894'],
            ['#E74C3C', '#E67E22', '#F1C40F', '#27AE60', '#2980B9'],
        ]
        return random.choice(palettes)
    
    def generate_carousel(self, brand_name: str, topic: str, 
                          template_type: str = 'tips', num_slides: int = 7) -> ContentPiece:
        """Generate a complete carousel post"""
        brand = self.brands.get(brand_name)
        if not brand:
            raise ValueError(f"Brand '{brand_name}' not found. Create it first.")
        
        template = self.CAROUSEL_TEMPLATES.get(template_type, self.CAROUSEL_TEMPLATES['tips'])
        
        # Generate hook
        hook = self._generate_hook(brand.industry, topic)
        
        # Generate slides
        slides = self._generate_slides(template, topic, num_slides, brand.voice)
        
        # Generate caption
        caption = self._generate_caption(brand, topic, hook)
        
        # Generate hashtags
        hashtags = self._generate_hashtags(brand.industry, topic)
        
        # Select CTA
        cta = self._select_cta(topic)
        
        # Calculate engagement score
        engagement_score = self._calculate_engagement_score(hook, slides, hashtags)
        
        # Determine best posting time
        best_time = self._optimal_posting_time(brand.target_audience)
        
        # Create title
        title_template = random.choice(template['titles'])
        title = self._fill_template(title_template, topic)
        
        return ContentPiece(
            content_type='carousel',
            title=title,
            slides=slides,
            caption=caption,
            hashtags=hashtags,
            hook=hook,
            cta=cta,
            engagement_score=engagement_score,
            best_posting_time=best_time,
            brand_voice=brand.voice
        )
    
    def _generate_hook(self, industry: str, topic: str) -> str:
        """Generate an attention-grabbing hook"""
        industry_hooks = self.HOOKS.get(industry, self.HOOKS['general'])
        hook_template = random.choice(industry_hooks)
        
        # Fill in the template
        variables = {
            'benefit': f'{topic} faster',
            'product': topic,
            'solution': f'the perfect {topic} strategy',
            'things': 'secrets',
            'action': f'starting {topic}',
            'opinion': f'{topic} is overrated',
            'problem': f'{topic} struggles',
            'topic': topic,
            'time': '10+ hours',
            'amount': '10K',
            'project': topic,
            'exercise': topic,
            'goal': f'better {topic}',
            'number': '5',
            'body_part': 'body',
            'dish': topic,
            'recipe': topic,
            'item': topic,
            'season': 'next year',
            'experience': f'{topic}',
            'start': 'zero',
            'end': 'hero',
            'cost': 'money',
            'action': 'doing this',
            'options': '1, 2, or 3?'
        }
        
        try:
            return hook_template.format(**variables)
        except KeyError:
            return hook_template.replace('{', '').replace('}', '')
    
    def _fill_template(self, template: str, topic: str) -> str:
        """Fill in template variables"""
        variables = {
            'number': random.choice(['3', '5', '7', '10']),
            'topic': topic.title(),
            'goal': f'Master {topic}',
            'start': 'Beginner',
            'end': 'Pro',
            'problem': f'{topic} issues',
            'action': topic,
            'cost': 'thousands'
        }
        try:
            return template.format(**variables)
        except KeyError:
            return template.replace('{', '').replace('}', '')
    
    def _generate_slides(self, template: Dict, topic: str, 
                         num_slides: int, voice: str) -> List[Dict]:
        """Generate carousel slides"""
        slides = []
        structure = template['structure'][:num_slides]
        
        slide_content = {
            'hook': {'type': 'hook', 'text': f'The {topic} secrets\neveryone needs 🔥', 'style': 'bold'},
            'intro': {'type': 'text', 'text': f'Here are the {topic}\nstrategies that\nactually work 👇', 'style': 'normal'},
            'tip_1': {'type': 'tip', 'number': 1, 'title': f'Start with research', 'text': f'Understand your {topic} before taking action'},
            'tip_2': {'type': 'tip', 'number': 2, 'title': f'Create systems', 'text': f'Build repeatable {topic} processes'},
            'tip_3': {'type': 'tip', 'number': 3, 'title': f'Measure results', 'text': f'Track what works in {topic}'},
            'tip_4': {'type': 'tip', 'number': 4, 'title': f'Scale winners', 'text': f'Double down on {topic} successes'},
            'bonus': {'type': 'bonus', 'title': '💡 Pro Tip', 'text': f'The best {topic} pros do this daily'},
            'cta': {'type': 'cta', 'text': f'Follow for more\n{topic} tips 🔥', 'style': 'cta'},
            'mistake_1': {'type': 'warning', 'number': 1, 'title': '❌ Random guessing', 'text': f'Never approach {topic} without a plan'},
            'mistake_2': {'type': 'warning', 'number': 2, 'title': '❌ Ignoring data', 'text': f'{topic} without metrics is just guessing'},
            'mistake_3': {'type': 'warning', 'number': 3, 'title': '❌ Giving up early', 'text': f'{topic} takes time - be patient'},
            'solution': {'type': 'solution', 'title': '✅ The Fix', 'text': f'Use this proven {topic} framework instead'},
            'step_1': {'type': 'step', 'number': 1, 'title': 'Research Phase', 'text': f'Analyze your {topic} situation thoroughly'},
            'step_2': {'type': 'step', 'number': 2, 'title': 'Strategy Phase', 'text': f'Create your {topic} action plan'},
            'step_3': {'type': 'step', 'number': 3, 'title': 'Execution Phase', 'text': f'Implement your {topic} strategy daily'},
            'step_4': {'type': 'step', 'number': 4, 'title': 'Optimization', 'text': f'Refine your {topic} approach weekly'},
            'result': {'type': 'result', 'title': '🎉 Results', 'text': f'Consistent {topic} growth within 90 days'},
            'pain_point': {'type': 'pain', 'title': f'Struggling with {topic}?', 'text': 'You\'re not alone - here\'s why...'},
            'results': {'type': 'result', 'title': 'The Results 📈', 'text': f'{topic} transformation in just 30 days'},
        }
        
        for slide_type in structure:
            if slide_type in slide_content:
                slides.append(slide_content[slide_type])
        
        return slides
    
    def _generate_caption(self, brand: BrandProfile, topic: str, hook: str) -> str:
        """Generate Instagram caption"""
        intros = [
            f"Let's talk about {topic}... 👇",
            f"Here's what nobody tells you about {topic}:",
            f"The {topic} game just changed 🔥",
            f"Real talk about {topic}:",
        ]
        
        value_props = [
            f"These {topic} strategies have worked for 100+ {brand.target_audience}.",
            f"I spent years figuring out {topic} so you don't have to.",
            f"This is the exact {topic} system we use.",
            f"Stop overcomplicating {topic}. Start here 👇",
        ]
        
        intro = random.choice(intros)
        value = random.choice(value_props)
        
        caption_parts = [
            hook,
            "",
            intro,
            "",
            value,
            "",
            "Save this post and come back to it when you need it 📌",
            "",
            f"Follow @{brand.name} for daily {topic} tips!",
        ]
        
        return '\n'.join(caption_parts)
    
    def _generate_hashtags(self, industry: str, topic: str) -> List[str]:
        """Generate optimized hashtag set"""
        # Get industry hashtags
        industry_tags = self.HASHTAGS.get(industry, self.HASHTAGS['general'])
        
        # Create topic-specific hashtags
        topic_tags = [
            f'#{topic.lower().replace(" ", "")}',
            f'#{topic.lower().replace(" ", "")}tips',
            f'#{topic.lower().replace(" ", "")}strategy',
        ]
        
        # Select best performing hashtags (mix of popular and niche)
        selected = random.sample(industry_tags[:5], min(3, len(industry_tags)))
        selected.extend(topic_tags)
        selected.extend(random.sample(self.HASHTAGS['general'][:5], 2))
        
        return list(set(selected))  # Remove duplicates
    
    def _select_cta(self, topic: str) -> str:
        """Select appropriate call-to-action"""
        cta = random.choice(self.CTAS)
        return cta.replace('{topic}', topic).replace('{keyword}', topic[:5].upper()).replace('{problem}', f'{topic} struggles')
    
    def _calculate_engagement_score(self, hook: str, slides: List[Dict], 
                                    hashtags: List[str]) -> int:
        """Predict engagement potential (0-100)"""
        score = 50  # Base score
        
        # Hook quality
        if any(char in hook for char in ['🔥', '💡', '😱', '👇']):
            score += 10
        if len(hook) < 60:
            score += 5
        
        # Slide count
        if 5 <= len(slides) <= 10:
            score += 15
        
        # Hashtag optimization
        if 8 <= len(hashtags) <= 15:
            score += 10
        
        return min(100, max(0, score))
    
    def _optimal_posting_time(self, target_audience: str) -> str:
        """Determine best posting time based on audience"""
        times = {
            'professionals': 'Tuesday/Thursday 12:00 PM or 5:00 PM',
            'entrepreneurs': 'Monday/Wednesday 8:00 AM or 6:00 PM',
            'students': 'Weekdays 7:00 PM - 9:00 PM',
            'parents': 'Weekdays 10:00 AM or 8:00 PM',
            'general': 'Tuesday-Thursday 11:00 AM - 1:00 PM',
        }
        return times.get(target_audience, times['general'])
    
    def generate_content_calendar(self, brand_name: str, days: int = 7) -> List[Dict]:
        """Generate a week's worth of content"""
        brand = self.brands.get(brand_name)
        if not brand:
            raise ValueError(f"Brand '{brand_name}' not found")
        
        calendar = []
        start_date = datetime.now()
        
        # Content mix: 60% carousels, 40% other
        content_types = ['carousel', 'carousel', 'carousel', 'single', 'reel', 'carousel', 'story']
        
        for i in range(min(days, len(brand.content_pillars) * 2)):
            date = start_date + timedelta(days=i)
            pillar = brand.content_pillars[i % len(brand.content_pillars)]
            
            content = self.generate_carousel(
                brand_name=brand_name,
                topic=pillar,
                template_type=random.choice(['tips', 'mistakes', 'steps'])
            )
            
            calendar.append({
                'date': date.strftime('%Y-%m-%d'),
                'day': date.strftime('%A'),
                'content_type': content.content_type,
                'title': content.title,
                'topic': pillar,
                'engagement_score': content.engagement_score,
                'best_time': content.best_posting_time,
                'caption_preview': content.caption[:100] + '...',
                'hashtags': content.hashtags,
            })
        
        return calendar
    
    def generate_single_post(self, brand_name: str, topic: str, 
                            post_type: str = 'educational') -> ContentPiece:
        """Generate a single image post"""
        brand = self.brands.get(brand_name)
        if not brand:
            raise ValueError(f"Brand '{brand_name}' not found")
        
        hook = self._generate_hook(brand.industry, topic)
        
        captions = {
            'educational': f"Quick {topic} tip:\n\n💡 [Insert educational content here]\n\nSave this for later! 📌",
            'motivational': f"Your daily reminder:\n\n🔥 [Insert motivational message about {topic}]\n\nTag someone who needs to hear this 👇",
            'promotional': f"Introducing [Product/Service]\n\n✨ The {topic} solution you've been waiting for\n\nLink in bio to learn more 👆",
            'engagement': f"Question for you:\n\n❓ [Insert engaging question about {topic}]\n\nDrop your answer below! 👇",
        }
        
        caption = captions.get(post_type, captions['educational'])
        hashtags = self._generate_hashtags(brand.industry, topic)
        
        return ContentPiece(
            content_type='single',
            title=f'{topic.title()} {post_type.title()}',
            slides=[{'type': 'single', 'style': post_type}],
            caption=caption,
            hashtags=hashtags,
            hook=hook,
            cta=self._select_cta(topic),
            engagement_score=random.randint(60, 90),
            best_posting_time=self._optimal_posting_time(brand.target_audience),
            brand_voice=brand.voice
        )
    
    def export_content(self, content: ContentPiece, format: str = 'json') -> str:
        """Export content in various formats"""
        if format == 'json':
            return json.dumps(asdict(content), indent=2)
        elif format == 'caption':
            return f"{content.caption}\n\n{' '.join(content.hashtags)}"
        elif format == 'slides':
            slides_text = []
            for i, slide in enumerate(content.slides, 1):
                slide_text = slide.get('text', slide.get('title', f'Slide {i}'))
                slides_text.append(f"Slide {i}:\n{slide_text}")
            return '\n\n'.join(slides_text)
        else:
            return str(content)
    
    def analyze_performance(self, content_history: List[Dict]) -> Dict:
        """Analyze past content performance and provide insights"""
        if not content_history:
            return {"error": "No content history provided"}
        
        avg_engagement = sum(c.get('engagement_score', 0) for c in content_history) / len(content_history)
        
        best_performing = max(content_history, key=lambda x: x.get('engagement_score', 0))
        
        insights = {
            'total_posts': len(content_history),
            'average_engagement_score': round(avg_engagement, 1),
            'best_performing_topic': best_performing.get('topic', 'Unknown'),
            'best_score': best_performing.get('engagement_score', 0),
            'recommendations': [
                f"Your content scores an average of {avg_engagement:.0f}/100",
                f"'{best_performing.get('topic', 'Unknown')}' performs best - create more content on this",
                "Consider posting more carousels - they typically perform 2x better",
                "Add more emojis to your hooks for higher engagement",
            ]
        }
        
        return insights


def demo():
    """Run a demo of the Content Forge"""
    print("=" * 70)
    print("🎨 BLAZE CONTENT FORGE - Demo")
    print("=" * 70)
    
    forge = ContentForge()
    
    # Create a sample brand
    print("\n1. Creating brand profile...")
    brand = forge.create_brand(
        name="BlazeIgnite",
        industry="marketing",
        voice="professional",
        target_audience="entrepreneurs",
        content_pillars=["email marketing", "shopify growth", "facebook ads", 
                        "automation", "client acquisition"],
        posting_frequency=5
    )
    print(f"   ✓ Created brand: {brand.name}")
    print(f"   ✓ Voice: {brand.voice}")
    print(f"   ✓ Content pillars: {', '.join(brand.content_pillars)}")
    
    # Generate a carousel
    print("\n2. Generating carousel post...")
    carousel = forge.generate_carousel(
        brand_name="BlazeIgnite",
        topic="email marketing",
        template_type="tips"
    )
    print(f"   ✓ Title: {carousel.title}")
    print(f"   ✓ Engagement Score: {carousel.engagement_score}/100")
    print(f"   ✓ Best Posting Time: {carousel.best_posting_time}")
    print(f"   ✓ {len(carousel.slides)} slides generated")
    
    # Show hook and caption
    print("\n3. Generated Content:")
    print(f"   Hook: {carousel.hook}")
    print(f"\n   Caption Preview:\n   {carousel.caption[:200]}...")
    print(f"\n   Hashtags: {' '.join(carousel.hashtags)}")
    
    # Show slide outline
    print("\n4. Slide Outline:")
    for i, slide in enumerate(carousel.slides, 1):
        slide_type = slide.get('type', 'content')
        text = slide.get('text', slide.get('title', f'Slide {i}'))
        print(f"   Slide {i} [{slide_type}]: {text[:50]}...")
    
    # Generate content calendar
    print("\n5. Content Calendar (Next 5 Days):")
    calendar = forge.generate_content_calendar("BlazeIgnite", days=5)
    for item in calendar:
        print(f"   {item['day']} ({item['date']}): {item['title']}")
        print(f"      Topic: {item['topic']} | Score: {item['engagement_score']}/100")
    
    # Generate single post
    print("\n6. Bonus Single Post:")
    single = forge.generate_single_post("BlazeIgnite", "facebook ads", "educational")
    print(f"   Type: {single.content_type}")
    print(f"   Hook: {single.hook}")
    print(f"   Caption: {single.caption[:150]}...")
    
    print("\n" + "=" * 70)
    print("✨ Demo complete! Content Forge is ready to use.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
