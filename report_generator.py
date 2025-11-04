"""
Report Generator - Creates consolidated PDF reports for both bots
"""
import os
import logging
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Optional

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics import renderPDF

from config import SYSTEM_NAMES, REPORTS_DIR
from data_collector import DataCollector

logger = logging.getLogger(__name__)

class ConsolidatedReportGenerator:
    def __init__(self):
        self.data_collector = DataCollector()
        
    def generate_report(self, report_type: str = "weekly") -> str:
        """
        Generate a consolidated monitoring PDF report
        
        Args:
            report_type: Type of report ("weekly" or "monthly")
            
        Returns:
            str: Path to the generated PDF file
        """
        try:
            # Fetch data from both bots
            stats = self.data_collector.get_combined_stats()
            trends = self.data_collector.get_daily_trends(30)
            
            # Create reports directory if it doesn't exist
            reports_path = Path(REPORTS_DIR)
            reports_path.mkdir(exist_ok=True)
            
            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"consolidated_monitoring_report_{report_type}_{timestamp}.pdf"
            filepath = reports_path / filename
            
            # Create PDF document
            doc = SimpleDocTemplate(
                str(filepath),
                pagesize=A4,
                rightMargin=50,
                leftMargin=50,
                topMargin=50,
                bottomMargin=50
            )
            
            # Build PDF content
            story = []
            
            # Page 1: Usage Statistics Tables
            story.extend(self._create_page1_tables(stats, report_type))
            
            # Page 2: Line Graphs
            story.append(PageBreak())
            story.extend(self._create_page2_graphs(trends))
            
            # Build the PDF
            doc.build(story)
            
            logger.info(f"Consolidated monitoring report generated: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error generating consolidated monitoring report: {e}")
            raise
    
    def _create_page1_tables(self, stats: Dict, report_type: str) -> List:
        """Create Page 1 content with usage statistics tables"""
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#000000'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#000000'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        elements.append(Paragraph("Usage Counts", title_style))
        elements.append(Paragraph(f"Consolidated {report_type.title()} Report (Daily / Weekly / Monthly)", subtitle_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Today's Table
        elements.append(self._create_section_table(
            "Today (Unique Users)",
            stats,
            "today"
        ))
        elements.append(Spacer(1, 0.5*inch))
        
        # This Week's Table
        elements.append(self._create_section_table(
            "This Week (Unique Users)",
            stats,
            "week"
        ))
        elements.append(Spacer(1, 0.5*inch))
        
        # This Month's Table
        elements.append(self._create_section_table(
            "This Month (Unique Users)",
            stats,
            "month"
        ))
        
        return elements
    
    def _create_section_table(self, title: str, stats: Dict, period: str) -> Table:
        """Create a single usage statistics table section"""
        styles = getSampleStyleSheet()
        
        # Section title
        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#000000'),
            spaceAfter=12
        )
        
        # Prepare table data
        dockify_count = stats["dockify"][period]
        tel_bot_count = stats["tel_bot"][period]
        invoice_count = stats["invoice"][period]
        travel_count = stats["travel"][period]
        document_count = stats["document"][period]
        total_count = stats["total"][period]
        
        data = [
            [Paragraph("<b>System</b>", styles['Normal']), 
             Paragraph("<b>Unique Users</b>", styles['Normal'])],
            [SYSTEM_NAMES["dockify"], str(dockify_count)],
            [SYSTEM_NAMES["tel_bot"], str(tel_bot_count)],
            [SYSTEM_NAMES["invoice"], str(invoice_count)],
            [SYSTEM_NAMES["travel"], str(travel_count)],
            [SYSTEM_NAMES["document"], str(document_count)],
            [Paragraph("<b>TOTAL</b>", styles['Normal']), 
             Paragraph(f"<b>{total_count}</b>", styles['Normal'])]
        ]
        
        # Create table
        table = Table(data, colWidths=[3.5*inch, 2*inch])
        
        # Style the table
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F0F0F0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows
            ('ALIGN', (0, 1), (0, -2), 'LEFT'),
            ('ALIGN', (1, 1), (1, -2), 'RIGHT'),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 12),
            ('BOTTOMPADDING', (0, 1), (-1, -2), 10),
            ('TOPPADDING', (0, 1), (-1, -2), 10),
            
            # Total row
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8E8E8')),
            ('ALIGN', (0, -1), (0, -1), 'LEFT'),
            ('ALIGN', (1, -1), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 10),
            ('TOPPADDING', (0, -1), (-1, -1), 10),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        # Add section title before table
        title_para = Paragraph(f"<b>{title}</b>", section_title_style)
        
        # Return as a combined element
        return Table([[title_para], [table]], colWidths=[5.5*inch])
    
    def _create_page2_graphs(self, trends: Dict) -> List:
        """Create Page 2 content with line graphs"""
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'GraphTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#000000'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        elements.append(Paragraph("Usage Trends", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # System Graphs
        section_title = ParagraphStyle(
            'GraphSectionTitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#000000'),
            spaceAfter=12
        )
        
        # DOCKFIY Bot Graph
        elements.append(Paragraph(f"<b>{SYSTEM_NAMES['dockify']} - Daily Active Users (Last 30 Days)</b>", section_title))
        if trends["dockify"] and len(trends["dockify"]) > 0:
            elements.append(self._create_line_chart(trends["dockify"], colors.HexColor('#3B82F6')))
        else:
            elements.append(Paragraph("No data available", styles['Normal']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Tel-Bot Graph
        elements.append(Paragraph(f"<b>{SYSTEM_NAMES['tel_bot']} - Daily Active Users (Last 30 Days)</b>", section_title))
        if trends["tel_bot"] and len(trends["tel_bot"]) > 0:
            elements.append(self._create_line_chart(trends["tel_bot"], colors.HexColor('#10B981')))
        else:
            elements.append(Paragraph("No data available", styles['Normal']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Invoice System Graph
        elements.append(Paragraph(f"<b>{SYSTEM_NAMES['invoice']} - Daily Active Users (Last 30 Days)</b>", section_title))
        if trends["invoice"] and len(trends["invoice"]) > 0:
            elements.append(self._create_line_chart(trends["invoice"], colors.HexColor('#F59E0B')))
        else:
            elements.append(Paragraph("No data available", styles['Normal']))
        
        # Travel System Graph
        elements.append(Paragraph(f"<b>{SYSTEM_NAMES['travel']} - Daily Active Users (Last 30 Days)</b>", section_title))
        if trends["travel"] and len(trends["travel"]) > 0:
            elements.append(self._create_line_chart(trends["travel"], colors.HexColor('#10B981')))
        else:
            elements.append(Paragraph("No data available", styles['Normal']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Document Bot Graph
        elements.append(Paragraph(f"<b>{SYSTEM_NAMES['document']} - Daily Active Users (Last 30 Days)</b>", section_title))
        if trends["document"] and len(trends["document"]) > 0:
            elements.append(self._create_line_chart(trends["document"], colors.HexColor('#8B5CF6')))
        else:
            elements.append(Paragraph("No data available", styles['Normal']))
        
        return elements
    
    def _create_line_chart(self, data: List[Dict], line_color) -> Drawing:
        """Create a line chart from data"""
        drawing = Drawing(400, 200)
        
        if not data or len(data) == 0:
            return drawing
        
        # Prepare data for chart
        values = [item['unique_users'] for item in data]
        
        # Create line chart
        chart = HorizontalLineChart()
        chart.x = 50
        chart.y = 30
        chart.height = 150
        chart.width = 350
        chart.data = [values]
        
        # Style the chart
        chart.lines[0].strokeColor = line_color
        chart.lines[0].strokeWidth = 2.5
        chart.lines[0].symbol = None
        
        # Configure axes
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(values) * 1.2 if values else 10
        chart.valueAxis.valueStep = max(1, int(max(values) / 5)) if values else 2
        
        # X-axis labels
        if len(data) > 0:
            label_interval = max(1, len(data) // 6)
            chart.categoryAxis.categoryNames = [
                datetime.fromisoformat(item['date']).strftime('%m/%d')
                if i % label_interval == 0 else ''
                for i, item in enumerate(data)
            ]
        
        # Grid and styling
        chart.categoryAxis.labels.angle = 45
        chart.categoryAxis.labels.fontSize = 8
        chart.valueAxis.labels.fontSize = 8
        
        drawing.add(chart)
        
        return drawing


# Helper function to be called from other modules
def generate_consolidated_report(report_type: str = "weekly") -> str:
    """
    Generate a consolidated monitoring report PDF
    
    Args:
        report_type: Type of report ("weekly" or "monthly")
        
    Returns:
        str: Path to the generated PDF file
    """
    generator = ConsolidatedReportGenerator()
    return generator.generate_report(report_type)
