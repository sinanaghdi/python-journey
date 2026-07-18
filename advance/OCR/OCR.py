from PIL import Image
import pytesseract
import pathlib
from googletrans import Translator
import time

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def process_images(folder="pic", lang="fas+eng", translate=False, save_output=True):
    """
    Process images with OCR and optional translation
    
    Args:
        folder: Folder containing images
        lang: OCR language ('fas', 'eng', 'fas+eng')
        translate: Enable translation to Persian
        save_output: Save results to file
    """
    translator = Translator()
    all_text = ""
    processed_count = 0
    error_count = 0
    
    print(f"🔍 Processing images in '{folder}' folder...")
    print("="*50)
    
    # Get all image files
    image_files = [p for p in pathlib.Path(folder).iterdir() 
                   if p.is_file() and p.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']]
    
    if not image_files:
        print("❌ No images found!")
        return
    
    for image_path in image_files:
        try:
            # Open and preprocess image
            img = Image.open(image_path)
            
            # Convert to grayscale for better accuracy
            if img.mode != 'L':
                img = img.convert('L')
            
            # Perform OCR
            extracted_text = pytesseract.image_to_string(img, lang=lang, config='--psm 6')
            
            if not extracted_text.strip():
                print(f"⚠️ {image_path.name}: No text found")
                continue
            
            # Add text to result
            all_text += f"File: {image_path.name}\n"
            all_text += f"Text: {extracted_text.strip()}\n"
            
            # Translate if requested
            if translate:
                try:
                    translated = translator.translate(extracted_text, dest='fa')
                    all_text += f"Translation: {translated.text}\n"
                    print(f"✅ {image_path.name}: OCR + Translation done")
                except Exception as e:
                    print(f"⚠️ {image_path.name}: Translation failed - {e}")
                    all_text += "Translation: Failed\n"
            else:
                print(f"✅ {image_path.name}: OCR done")
            
            all_text += 50 * "=" + "\n"
            processed_count += 1
            
            # Small delay to avoid rate limiting on translation
            if translate:
                time.sleep(0.5)
                
        except Exception as e:
            error_count += 1
            print(f"❌ {image_path.name}: Error - {e}")
    
    # Print summary
    print("="*50)
    print(f"📊 Summary: {processed_count} images processed, {error_count} errors")
    
    # Save to file
    if save_output and all_text:
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(all_text)
        print("💾 Results saved to output.txt")
    
    # Display results
    print("\n📝 Extracted Text:")
    print("-"*50)
    print(all_text)
    
    return all_text

# Main execution
if __name__ == "__main__":
    # Configuration
    LANGUAGE = "fas+eng"  # or "eng", "fas"
    FOLDER = "pic"
    TRANSLATE = input("Do you want to translate to Persian? (y/n): ").lower() == 'y'
    
    process_images(folder=FOLDER, lang=LANGUAGE, translate=TRANSLATE)