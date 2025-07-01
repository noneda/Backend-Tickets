def categorized_upload_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    extension_map = {
        "videos": ["mp4", "avi", "mov", "mkv"],
        "images": ["jpg", "jpeg", "png", "gif", "webp"],
        "documents": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt"],
        "compressed": ["zip", "rar", "7z"],
        "audio": ["mp3", "wav", "ogg"],
    }

    for category, extensions in extension_map.items():
        if ext in extensions:
            subdir = category
            break
    else:
        subdir = "others"

    return f"{instance.secretariat.name}/{subdir}/{filename}"
