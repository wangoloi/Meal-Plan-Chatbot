import os
from app import create_app

def main():
	app = create_app()
	debug = os.getenv('FLASK_ENV', 'development') != 'production'
	app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=debug)

if __name__ == '__main__':
	main()

