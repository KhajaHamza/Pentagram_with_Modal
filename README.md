# Pentagram

A text-to-image generation web application powered by Stable Diffusion XL Turbo and Modal's GPU infrastructure.

## Setup Guide

### Frontend Setup

1. Clone the GitHub repository:
```bash
git clone https://github.com/KhajaHamza/Pentagram_with_Modal.git
```

2. Navigate to the project directory:
```bash
cd pentagram
```

3. Install dependencies:
```bash
npm install
```

4. Run the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Backend (Modal) Setup

#### Virtual Environment Setup
Create and activate a Python virtual environment:

**macOS/Linux**:
```bash
python -m venv venv
source venv/bin/activate
```

**Windows**:
```bash
python -m venv venv
.\venv\Scripts\activate
```

#### Modal Configuration

1. Create an account at [modal.com](https://modal.com)

2. Install Modal in your virtual environment:
```bash
pip install modal
```

3. Authenticate with Modal:
```bash
modal token new
```
This will open a browser window for login and token authorization.

4. Deploy your Modal application:
```bash
modal deploy main.py
```

**Note**: If you encounter authentication issues, try:
```bash
python -m modal setup
```

## Important Reminders
- Always activate your virtual environment before working with Modal
- Keep your Modal token secure
- Make sure both frontend and backend are running for full functionality
- Use Your GPU Credits Wisely

## Contributing
Feel free to open issues and submit pull requests.

