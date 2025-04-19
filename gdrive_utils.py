import io
import os
import pickle
import re

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from config import CREDENTIALS_FILE, TOKEN_FILE, SCOPES


def authenticate_drive():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


def extract_file_id(drive_url):
    file_match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', drive_url)
    folder_match = re.search(r'/folders/([a-zA-Z0-9_-]+)', drive_url)

    if file_match:
        return file_match.group(1)
    elif folder_match:
        return folder_match.group(1)
    else:
        raise ValueError("URL do Google Drive inválida ou não reconhecida.")


def download_file(file_id, destination_path, service):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    print(f"✅ Download concluído: {destination_path}")


def find_file_id_by_name(service, folder_name, file_prefix):
    # 1. Busca o ID da pasta
    folder_query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
    folders = service.files().list(q=folder_query, fields="files(id)").execute()
    if not folders['files']:
        print(f"❌ Pasta '{folder_name}' não encontrada.")
        return None
    folder_id = folders['files'][0]['id']

    # 2. Busca o arquivo pelo prefixo dentro da pasta
    file_query = f"'{folder_id}' in parents and name contains '{file_prefix}' and trashed = false"
    files = service.files().list(q=file_query, fields="files(id, name)").execute()

    if not files['files']:
        print(f"❌ Nenhum arquivo encontrado com prefixo '{file_prefix}' na pasta '{folder_name}'.")
        return None

    file = files['files'][0]
    print(f"✅ Arquivo encontrado: {file['name']}")
    return file['id']
