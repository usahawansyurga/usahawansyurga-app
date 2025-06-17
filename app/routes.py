from flask import Blueprint, render_template
from .ai import scan_market

main = Blueprint('main', __name__)

@main.route('/')
def index():
    signals = scan_market()
    return render_template('index.html', signals=signals)

