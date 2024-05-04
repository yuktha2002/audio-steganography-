from fastapi import APIRouter, HTTPException, Form, Depends, UploadFile, File
from app import get_current_user
from app import merge_text_and_wav, decrypt_and_get_text

router = APIRouter(prefix='/encode_decode')


@router.post('/encrypt_waveform_text',
             tags=['Encode'],
             status_code=200)
def encrypt_data(waveform_file: UploadFile = File(...),
                 text: str = Form(...),
                 current_user: int = Depends(get_current_user)):
    file_type = True if waveform_file.filename.split(
        '.')[-1] == 'wav' else False
    if file_type is False:
        raise HTTPException(
            detail='please insert waveform file', status_code=402)
    return merge_text_and_wav(
        text, waveform_file.file, f'merged_{waveform_file.filename}')


@router.get('/decrypt_waveform_file/{file_name}',
            status_code=200,
            tags=['Decode'])
def decrypt_file(file_name: str,
                 current_user: int = Depends(get_current_user)):
    text_decrypted = decrypt_and_get_text(file_name)
    return {'decrypted_test': text_decrypted}
