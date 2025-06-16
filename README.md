
# MuniAPMs Task Scheduler

A professional Streamlit web application for managing weekly task assignments across team members, designed specifically for MuniAPMs company.

## Features

- **User-Friendly Interface**: Intuitive web interface with MuniAPMs branding
- **Availability Management**: Easy input for team member availability and company holidays
- **Smart Scheduling**: Automated task assignment with fairness and constraint handling
- **Multiple Views**: Task-by-day and person-by-day schedule views
- **Export Functionality**: Download schedules as CSV files
- **Real-time Statistics**: Workload distribution metrics
- **Responsive Design**: Works on desktop and mobile devices

## Team Configuration

**Team Members**: MG, Anna, Zi, Dan, Max, Mark

**Tasks**:
- Opti (Urgent and Standard) - Weight: 3
- Sizing - Weight: 2
- 1st & 2nd File, 2nd round raises - Weight: 3
- Algo sales, Review 2nd round raises - Weight: 2
- Review AM Raises, 3rd file - Weight: 2

**Constraints**:
- Zi and Mark cannot do Sizing tasks
- Schedule covers Monday-Friday only

## Installation & Usage

### For Streamlit Cloud Deployment

1. Fork this repository
2. Connect to Streamlit Cloud
3. Deploy directly from GitHub

### For Local Development

1. Install Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## How to Use

1. **Set Availability**: Select days when team members are unavailable
2. **Add Holidays**: Mark company-wide holidays
3. **Generate Schedule**: Click to create the weekly schedule
4. **Review & Export**: Download CSV files for external use

## Scheduling Algorithm

The scheduler uses a multi-tier priority system:

1. **Daily Balance**: People with 0 tasks today get first priority
2. **Task Diversity**: Among equals, those who haven't done the specific task
3. **Load Balancing**: When all else equal, choose least loaded person
4. **Random Selection**: Final tie-breaker to avoid bias

## Technical Details

- Built with Streamlit for easy deployment
- Uses pandas for data manipulation
- Implements fair task distribution algorithms
- Supports CSV export for external tools
- Optimized for small teams (<10 people)

## Support

For technical support or feature requests, contact the MuniAPMs IT team.

## License

Internal use only - MuniAPMs Company
