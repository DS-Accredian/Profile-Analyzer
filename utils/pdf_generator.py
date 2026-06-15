from fpdf import FPDF
import io

class LinkedBoostPDF(FPDF):
    def header(self):
        # Modern Blue Header
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(26, 115, 232)
        self.cell(0, 10, 'LinkedBoost Profile Blueprint', border=0, ln=1, align='C')
        self.set_line_width(0.5)
        self.set_draw_color(200, 200, 200)
        self.line(10, 22, 200, 22)
        self.ln(10)

    def footer(self):
        # Gray Footer
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', border=0, align='C')

def sanitize_text(text):
    """Replaces smart quotes and unsupported characters for standard PDF fonts."""
    if not text:
        return ""
    
    text = str(text)
    # Fix standard typographical marks
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-").replace("…", "...")
    
    # CRITICAL FIX: Replace tabs and non-breaking spaces that confuse the PDF wrapper
    text = text.replace('\t', '    ').replace('\xa0', ' ')
    
    return text.encode('latin-1', 'replace').decode('latin-1')

def generate_blueprint_pdf(health_score, critical_gaps, recommended_prompts):
    pdf = LinkedBoostPDF()
    
    # Explicitly define all margins to ensure the math never fails
    pdf.set_margins(left=15, top=15, right=15)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Calculate the exact usable width of the page (epw)
    epw = pdf.w - 30 # 15 left margin + 15 right margin
    
    # --- SECTION 1: PROFILE AUDIT SUMMARY ---
    pdf.set_font("Helvetica", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(epw, 10, "1. Profile Audit Summary", ln=1)
    
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_text_color(26, 115, 232)
    pdf.cell(epw, 8, f"Health Score: {health_score}/100", ln=1)
    pdf.ln(2)
    
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(epw, 8, "Top Critical Gaps:", ln=1)
    
    pdf.set_font("Helvetica", '', 11)
    pdf.set_x(15) # Force cursor to left margin
    pdf.multi_cell(epw, 6, sanitize_text(critical_gaps))
    pdf.ln(8)
    
    # --- SECTION 2: TACTICAL REWRITE PROMPTS ---
    pdf.set_font("Helvetica", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(epw, 10, "2. Tactical Rewrite Prompts", ln=1)
    
    pdf.set_font("Helvetica", '', 11)
    pdf.set_x(15)
    pdf.multi_cell(epw, 6, "Copy and paste these exact prompts into your AI tool to rewrite your profile sections and resolve your critical gaps.")
    pdf.ln(6)

    for idx, prompt in enumerate(recommended_prompts, 1):
        pdf.set_x(15) # Force cursor to left margin before every new prompt
        
        # Prompt Title
        pdf.set_font("Helvetica", 'B', 12)
        pdf.set_text_color(26, 115, 232)
        pdf.cell(epw, 8, sanitize_text(f"Prompt {idx}: {prompt.get('title', 'N/A')}"), ln=1)
        pdf.set_text_color(0, 0, 0)
        
        # Prompt Description
        pdf.set_font("Helvetica", 'I', 10)
        pdf.set_x(15)
        pdf.multi_cell(epw, 6, sanitize_text(f"Why use this: {prompt.get('description', '')}"))
        pdf.ln(2)
        
        # Prompt Code Block
        pdf.set_font("Courier", '', 9)
        pdf.set_fill_color(245, 245, 245)
        pdf.set_x(15)
        pdf.multi_cell(epw, 5, sanitize_text(prompt.get("prompt", "")), fill=True)
        pdf.ln(3)
        
        # Pro Tips
        pro_tips = prompt.get("pro_tips", [])
        if pro_tips:
            pdf.set_x(15)
            pdf.set_font("Helvetica", 'B', 10)
            pdf.cell(epw, 6, "Pro Tips:", ln=1)
            pdf.set_font("Helvetica", '', 10)
            
            for tip in pro_tips:
                pdf.set_x(15) # Ensure bullet points don't drift to the right
                pdf.multi_cell(epw, 5, sanitize_text(f"- {tip}"))
        
        pdf.ln(8)

    # Return the raw bytes of the PDF
    return bytes(pdf.output())