#!/usr/bin/env python3
"""
Test script to verify Pexels image generation
Run this to check if images are loading from Pexels API
"""

import sys
import requests
sys.path.insert(0, 'backend')

from images import generate_images_with_metadata, get_pexels_image_url, get_fallback_image_url

def test_pexels_api():
    """Test Pexels API connectivity and image retrieval"""
    print("\n🔍 Testing Pexels API...\n")
    
    test_query = "peaceful nature"
    url = get_pexels_image_url(test_query, 0)
    
    print(f"Test Query: '{test_query}'")
    print(f"Generated URL: {url[:80]}...")
    
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            print(f"✅ Pexels API working! (HTTP {response.status_code})")
            print(f"   Content-Type: {response.headers.get('content-type', 'image')}")
            return True
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️  Pexels API not responding: {e}")
        return False

def test_fallback_images():
    """Test fallback image service"""
    print("\n🔍 Testing Fallback Image Service...\n")
    
    url = get_fallback_image_url("test")
    print(f"Fallback URL: {url}")
    
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            print(f"✅ Fallback service working! (HTTP {response.status_code})")
            return True
    except Exception as e:
        print(f"❌ Fallback error: {e}")
        return False

def test_image_generation():
    """Test that images are generated with correct URLs"""
    print("\n🔍 Testing Image Generation (Full Pipeline)...\n")
    
    images = generate_images_with_metadata("test message")
    
    for i, img in enumerate(images, 1):
        print(f"Image {i}: {img['emoji']} {img['mood_type'].upper()}")
        print(f"  Description: {img['description']}")
        print(f"  URL: {img['url'][:60]}...")
        
        # Try to access the image
        try:
            response = requests.head(img['url'], timeout=5, allow_redirects=True)
            if response.status_code == 200:
                content_type = response.headers.get('content-type', 'unknown')
                if 'image' in content_type.lower():
                    print(f"  ✅ Valid image ({content_type})")
                else:
                    print(f"  ⚠️  Content-Type: {content_type}")
            else:
                print(f"  ⚠️  HTTP {response.status_code}")
        except requests.Timeout:
            print(f"  ⚠️  Timeout (network issue)")
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:50]}")
        
        print()

def test_api_endpoint():
    """Test the backend /images endpoint"""
    print("\n🔍 Testing Backend /images Endpoint...\n")
    
    try:
        response = requests.get("http://localhost:8000/images", timeout=5)
        
        if response.status_code == 200:
            images = response.json()
            print(f"✅ Backend /images endpoint working\n")
            
            for i, img in enumerate(images, 1):
                print(f"Image {i}: {img['emoji']} {img['mood_type'].upper()}")
                print(f"  URL: {img['url'][:60]}...")
                
        else:
            print(f"❌ Backend returned HTTP {response.status_code}")
            
    except requests.ConnectionError:
        print("❌ Cannot connect to backend at http://localhost:8000")
        print("   Start it: uvicorn backend.main:app --reload --port 8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("=" * 70)
    print("MENTAL CHATBOT - PEXELS IMAGE GENERATION TEST")
    print("=" * 70)
    
    # Test Pexels API
    pexels_ok = test_pexels_api()
    
    # Test fallback
    test_fallback_images()
    
    # Test full pipeline
    test_image_generation()
    
    # Test backend endpoint
    test_api_endpoint()
    
    print("\n" + "=" * 70)
    print("RESULTS:")
    print("=" * 70)
    if pexels_ok:
        print("✅ Pexels API is working - images should load from Pexels")
    else:
        print("⚠️  Pexels API not responding - fallback images will be used")
    print("\nTo run the full application:")
    print("  Terminal 1: uvicorn backend.main:app --reload --port 8000")
    print("  Terminal 2: streamlit run frontend/app.py")
    print("=" * 70)
