import ast
from passlib.context import CryptContext
import wave
from fastapi import HTTPException


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hass_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_text: str, hashpassword):
    return pwd_context.verify(plain_text, hashpassword)


def merge_text_and_wav(text_file,
                       wav_file,
                       output_file):
    try:
        text_content = text_file
        with wave.open(wav_file, 'rb') as wav_obj:
            wav_info = {
                "sample_rate": wav_obj.getnframes(),
                "channels": wav_obj.getnchannels(),
                "sample_width": wav_obj.getsampwidth()
            }
        merged_data = {
            "text": text_content,
            "audio_info": wav_info
        }
        with open(f'outputfile/{output_file}', 'w') as f:
            f.write(str(merged_data))

        return {'encrypted': 'True',
                'file_name': f"Merged data saved to: {output_file}"}
    except Exception as e:
        HTTPException(status_code=500,
                      detail=f'Could not encrypt the file {type(e).__name__}')


def decrypt_and_get_text(merged_file):
    try:
        def decrypt_text(text):
            return f"{text}"
        with open(f'outputfile/{merged_file}', 'r') as f:
            merged_data = ast.literal_eval(f.read())
        return decrypt_text(merged_data["text"])
    except Exception as e:
        HTTPException(status_code=500,
                      detail=f'Could not encrypt the file {type(e).__name__}')
