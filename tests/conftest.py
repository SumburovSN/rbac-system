import sys
from pathlib import Path
from dotenv import load_dotenv

# Добавляем корень проекта в PYTHONPATH
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

load_dotenv('tests/.env.test')
