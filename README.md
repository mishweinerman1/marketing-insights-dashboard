# Marketing Insights Dashboard

An interactive Dash (Python/React) dashboard that transforms marketing analysis Excel files into beautiful, actionable visualizations. Built for marketing consultants to pitch data-driven strategies to clients.

## Features

- **📊 Executive Summary**: 4-channel revenue breakdown with key insights
- **📈 Overall Performance**: Traffic analysis, engagement metrics, and competitive positioning
- **🎯 Tactics Matrix**: Effort vs. impact prioritization for marketing initiatives
- **🔍 Channel Deep Dives**: Dedicated analysis for Paid Search, SEO, CRM, CRO
- **🎨 Template-Based Branding**: Easy customization for different clients
- **📤 Excel File Upload**: Drag-and-drop interface for data ingestion

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/[your-username]/marketing-insights-dashboard.git
cd marketing-insights-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard

```bash
# Start the Dash server
python app.py

# Open browser to http://localhost:8050
```

## Usage

1. **Upload Excel File**: Drag and drop your marketing analysis Excel file
2. **Explore Data**: Navigate through Executive Summary, Performance, and Tactics sections
3. **Customize Branding**: Edit `config/branding.py` to add client themes
4. **Export**: Share insights with interactive visualizations

## Required Excel File Structure

Your Excel file should contain these sheets:

- **Similarweb Lead Enrichment** - Traffic data over time
- **Similarweb PPC Spend** - Paid advertising spend
- **Low Hanging Fruit** - Marketing tactics with effort/cost/lift
- **IE Matrix** - Implementation/Effort scores
- **Core Web Vitals** - Website performance metrics
- **Keyword Reports** - Paid and organic keyword data

## Project Structure

```
marketing-insights-dashboard/
├── app.py                     # Main application
├── config/
│   └── branding.py            # Client theming system
├── data/
│   ├── loader.py              # Excel file parsing
│   ├── processor.py           # Data transformation
│   └── validators.py          # Data validation
├── components/
│   ├── header.py              # Branded header
│   ├── metric_cards.py        # Summary cards
│   └── charts.py              # Plotly visualizations
├── layouts/
│   ├── executive_summary.py   # Executive summary page
│   ├── overall_performance.py # Performance analysis page
│   └── tactics_matrix.py      # Tactics prioritization page
├── callbacks/
│   ├── data_upload.py         # File upload handling
│   └── navigation.py          # Page routing
└── assets/
    └── styles.css             # Custom CSS
```

## Customization

### Adding a New Client Theme

Edit `config/branding.py`:

```python
theme = ClientBranding.customize(
    'client_template',
    client_name='Your Client',
    primary_color='#0066CC',
    secondary_color='#003D7A',
    logo_path='/assets/logos/client.png'
)
```

### Adding New Visualizations

1. Add chart function to `components/charts.py`
2. Import and use in layout files
3. Update callbacks if interactive filtering needed

## Deployment

### Render.com

```yaml
# render.yaml
services:
  - type: web
    name: marketing-insights-dashboard
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:server
```

### Heroku

```bash
# Create Procfile
echo "web: gunicorn app:server" > Procfile

# Deploy
heroku create
git push heroku main
```

## Tech Stack

- **Dash 3.2.0** - Python framework for building web applications
- **Plotly 6.4.0** - Interactive visualization library
- **Pandas 2.3.3** - Data manipulation and analysis
- **Bootstrap 5** - Responsive UI components

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this for your own marketing analysis projects.

## Acknowledgments

- Built with Dash by Plotly
- Design inspired by modern SaaS dashboards
- Data processing patterns from marketing analytics best practices

---

**Built with ❤️ by [Your Name] for AUX Insights**
