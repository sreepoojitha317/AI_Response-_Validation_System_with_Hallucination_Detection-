from app.report.dashboard_pdf import generate_dashboard_pdf


generate_dashboard_pdf(

    "http://127.0.0.1:8000/dashboard/pdf",

    "Evaluation_Dashboard.pdf"

)


print("Dashboard PDF Generated Successfully")