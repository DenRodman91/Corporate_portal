🎨 Marketplace Sales & Feedback Management Dashboard

Welcome to the Marketplace Sales & Feedback Management Dashboard! This is a web application designed to streamline marketplace operations, providing insightful dashboards, automated data processing, and powerful integrations for efficient workflow management.

🧰 Features

	•	📊 Sales Dashboards: Interactive dashboards to visualize sales performance and logistics.
	•	🔗 Google Sheets Integration: Seamless data export and import with Google Sheets.
	•	🛒 Marketplace Data Processing: Efficient handling of sales, logistics, and product categories for Wildberries, Ozon, and other marketplaces.
	•	📝 Feedback Management: Automated feedback collection and response system with support for multiple tokens.
	•	🤖 Telegram Notifications: Real-time alerts and notifications to Telegram using the Bot API.
	•	⚙️ Automated Scripts: Subprocess execution for scheduled tasks like data syncing, report generation, and more.

🚀 Technologies

	•	Flask: Backend framework for routing and server management.
	•	Dash: For creating interactive and responsive data visualizations.
	•	SQLite & MySQL: Relational databases for storing user data and reports.
	•	Pandas: Data processing and manipulation library.
	•	gspread & Google Sheets API: For Google Sheets interaction.
	•	Plotly: Data visualization library for generating interactive plots.
	•	TeleBot: Telegram Bot API integration for notifications.

🏗️ Project Structure
📂 Marketplace-Dashboard
├── app.py               # Main Flask application
├── dashboard_app.py      # Dash application for data visualization
├── processing.py         # Data processing logic for marketplace reports
├── all_otzivi.py         # Feedback management and response automation
├── to_google.py          # Integration with Google Sheets API
├── static/               # Static files (CSS, images, etc.)
├── templates/            # HTML templates for rendering pages
└── requirements.txt      # Dependencies

📖 Installation
git clone https://github.com/yourusername/marketplace-dashboard.git
pip install -r requirements.txt
python app.py

🛠️ Usage

	•	Access the dashboard by navigating to http://127.0.0.1:5010/.
	•	Login using predefined users to access the various features.
	•	Use the upload section to process marketplace data and generate reports.
	•	Automatically send and respond to feedback from Wildberries using the integrated feedback bot.

🛡️ Security

	•	Ensure that API tokens, sensitive keys, and credentials are stored securely in environment variables or a secure vault.
	•	Use HTTPS for secure communication when deploying to production.

📈 Visuals

Sales Dashboard Example

✍️ Contributing

We welcome contributions! Feel free to fork the project, submit issues, or open pull requests.

📝 License

This project is licensed under the MIT License.

✨ Acknowledgements

	•	Special thanks to the developers and libraries that made this project possible, including Flask, Dash, Plotly, and gspread.
