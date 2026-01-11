import requests
import os

BASE_URL = "http://localhost:8000"

def test_photo_flow():
    # 1. Register/Login
    email = "test_photo@example.com"
    password = "password123"
    
    # Try register
    try:
        resp = requests.post(f"{BASE_URL}/auth/register", json={
            "email": email,
            "password": password,
            "name": "Test User",
            "role": "admin" 
        })
    except Exception as e:
        print(f"Register failed (maybe exists): {e}")

    # Login
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return
    
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Logged in.")

    # 2. Create Site
    site_resp = requests.post(f"{BASE_URL}/sites", json={
        "name": "Test Site",
        "address": "123 Test St",
        "latitude": 10.0,
        "longitude": 20.0,
        # We need valid property/facility managers. 
        # For simplicity, we'll try to use the current user ID if endpoints accept self,
        # But wait, create_site expects 'property_manager' (int) and 'facility_manager' (int).
        # We need their IDs.
        # Let's get "me" to find my ID.
    }, headers=headers)
    
    # Get Me
    me_resp = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    my_id = me_resp.json()["id"]
    
    # Retry Create Site with correct IDs
    site_payload = {
        "name": "Test Site",
        "address": "123 Test St",
        "latitude": 10.0,
        "longitude": 20.0,
        "property_manager": my_id,
        "facility_manager": my_id
    }
    site_resp = requests.post(f"{BASE_URL}/sites", json=site_payload, headers=headers)
    if site_resp.status_code != 200:
        print(f"Create site failed: {site_resp.text}")
        # If site creation fails (e.g. maybe 422), we might need to look at what happened.
        # But let's assume it works or we use an existing site.
        # If it failed, maybe we can list sites and pick one.
        sites_resp = requests.get(f"{BASE_URL}/sites", headers=headers)
        if sites_resp.json():
            site_id = sites_resp.json()[0]["id"]
            print(f"Using existing site {site_id}")
        else:
            print("No sites available and create failed.")
            return
    else:
        site_id = site_resp.json()["id"]
        print(f"Created site {site_id}")

    # 3. Create Task
    task_resp = requests.post(f"{BASE_URL}/tasks", json={
        "site_id": site_id,
        "title": "Photo Test Task",
        "description": "Testing photo upload",
        "priority": 3,
        "status": "TODO"
    }, headers=headers)
    
    if task_resp.status_code != 200:
        print(f"Create task failed: {task_resp.text}")
        return
    
    task_id = task_resp.json()["id"]
    print(f"Created task {task_id}")

    # 4. Upload Photo
    # Create a dummy image file
    with open("test_image.png", "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82")

    files = {'file': ('test_image.png', open('test_image.png', 'rb'), 'image/png')}
    upload_resp = requests.post(
        f"{BASE_URL}/tasks/{task_id}/photos",
        headers={"Authorization": f"Bearer {token}"}, # Don't set Content-Type, requests does it for multipart
        files=files
    )
    
    if upload_resp.status_code != 200:
        print(f"Upload failed: {upload_resp.text}")
        return
        
    print(f"Upload response: {upload_resp.json()}")
    
    # 5. List Photos
    list_resp = requests.get(f"{BASE_URL}/tasks/{task_id}/photos", headers=headers)
    photos = list_resp.json()["photos"]
    print(f"Photos list: {photos}")
    
    if not photos:
        print("No photos found in list!")
        return

    photo_id = photos[0]["id"]
    
    # 6. Download Photo
    dl_resp = requests.get(f"{BASE_URL}/tasks/{task_id}/photos/{photo_id}", headers=headers)
    if dl_resp.status_code == 200:
        print(f"Download success, size: {len(dl_resp.content)} bytes")
    else:
        print(f"Download failed: {dl_resp.status_code}")

    # Clean up
    if os.path.exists("test_image.png"):
        os.remove("test_image.png")

if __name__ == "__main__":
    test_photo_flow()
