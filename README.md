# Weekly Task Update Dashboard

This Streamlit-based dashboard provides an overview of weekly updates, including product roadmap insights, key requirements, market insights, and group task updates. The data is fetched dynamically from Airtable using the PyAirtable library.

---

## Features

### 1. **Product Roadmap**
Displays updates on the product roadmap, including features, baseline completion time, and estimated actual completion time. 

### 2. **Key Requirements Management**
Summarizes meeting minutes and requirements managed during RMT meetings, categorized by region, status, and priority.

### 3. **Prototype Management**
Links to relevant resources for prototype updates.

### 4. **Testing Plan Roadmap**
Provides a link to the testing plan for easy access to further details.

### 5. **Market Insights & Product Document Updates**
Summarizes weekly market insights and product documentation updates, with additional links to Chinese and English versions.

### 6. **Weekly Team Task Updates**
Highlights key RAID (Risks, Assumptions, Issues, Dependencies) items updated for the week.

---

## How to Run

### Prerequisites
Ensure you have the following installed:
- Python 3.9+
- Streamlit
- PyAirtable
- Pandas

### Setup
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up Airtable credentials:
   - Add an `AT_API_KEY` to your `secrets.toml` file in the Streamlit configuration folder.

### Run the Dashboard
```bash
streamlit run app.py
```

---

## Files

- **app.py**: Main dashboard application code.
- **requirements.txt**: List of Python dependencies.

---

## Data Sources
Data is fetched from the following Airtable tables:
- `欧洲产品路线图` (Product Roadmap)
- `Requirement List`
- `市场洞察` (Market Insights)
- `产品资料库更新LOG` (Product Document Log)
- `团队任务` (Weekly Team Task Updates)

---

## Acknowledgements
Special thanks to the team members contributing insights for weekly updates.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
