# Quick Start Guide - ZOE NutriTech

## Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
DATABASE_URL=sqlite:///zoenutritech.db
```

### Step 3: Run the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

### Step 4: Create Your First Account

1. Go to `http://localhost:5000`
2. Click "Get Started" or "Register"
3. Create an account with username, email, and password
4. Complete the onboarding form with your health information

### Step 5: Explore Features

- **Dashboard**: View your health overview
- **Recommendations**: Get personalized food recommendations
- **Search**: Search for foods in the database
- **Chat Assistant**: Ask questions about nutrition
- **Goals**: Set and track health goals
- **Diabetes Dashboard**: (If you have diabetes) Track your diabetes management

## Common Tasks

### Getting Food Recommendations

1. Go to "Recommendations" in the navigation
2. Select a meal type (breakfast, lunch, dinner, snack)
3. View recommended foods with explanations
4. Accept or reject recommendations

### Searching for Foods

1. Go to "Search Foods" in the navigation
2. Type a food name (e.g., "matooke", "beans")
3. Use filters to narrow results
4. View nutritional information

### Using the Chat Assistant

1. Go to "Chat Assistant" in the navigation
2. Type your question (e.g., "What should I eat for breakfast?")
3. Get instant nutrition advice
4. Ask follow-up questions

### Tracking Diabetes (If Applicable)

1. Go to "Diabetes" in the navigation
2. Click "Record Blood Glucose"
3. Enter your reading
4. View progress and statistics

### Setting Goals

1. Go to "Goals" in the navigation
2. Click "Create New Goal"
3. Set your target (weight, blood glucose, etc.)
4. Update progress regularly

## Troubleshooting

### Database Issues

If you encounter database errors:
```bash
# Delete existing database
rm zoenutritech.db

# Restart application (database will be recreated)
python run.py
```

### Port Already in Use

If port 5000 is already in use:
```bash
# Set a different port
export PORT=5001  # Linux/Mac
set PORT=5001     # Windows

python run.py
```

### Missing Dependencies

If you get import errors:
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [docs/](docs/) for system-specific documentation
- Customize the system for your needs
- Deploy to production (see README.md)

## Support

For issues or questions:
- Check the documentation in `docs/`
- Review error messages
- Check application logs

---

**Happy Healthy Eating! 🥗**

