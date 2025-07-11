BUTTON_STYLE_CHOICES = [
    ('black', 'Black'),
    ('white', 'White'),
    ('blue', 'Blue'),
]

VISIBLE_CHOICES = (
    ('all', 'All Users'),
    ('anonymous', 'Only Anonymous'),
    ('authenticated', 'Only Logged-in'),
)

POSITION_CHOICES = (
    ('left', 'Left'),
    ('right', 'Right'),
)

LINK_TYPE_CHOICES = [
    ('module', 'Module (Named URL)'),
    ('cms', 'CMS Page'),
    ('external', 'External URL'),
]

# SME_FORM_WIZARD_CHOICES
BUSINESS_SIZES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]

INDUSTRY_SECTORS = [
    ('tech', 'Technology'),
    ('finance', 'Finance'),
    ('retail', 'Retail'),
    ('agriculture', 'Agriculture'),
    ('healthcare', 'Healthcare'),
    ('others', 'Others'),
    
    # Add more as needed
]

LEGAL_TYPES = [
    ('sole', 'Sole Proprietorship'),
    ('partnership', 'Partnership'),
    ('llc', 'Limited Liability Company (LLC)'),
    ('corporation', 'Corporation'),
]

BUSINESS_STAGES = [
    ('ideation', 'Ideation'),
    ('early', 'Early Stage'),
    ('growth', 'Growth'),
    ('mature', 'Mature'),
]

OWNERSHIP_TYPES = [
    ('private', 'Private'),
    ('public', 'Public'),
    ('ngo', 'Non-Profit / NGO'),
]

SERVICE_TYPES = [
    ('consulting', 'Consulting'),
    ('development', 'Development'),
    ('marketing', 'Marketing'),
    ('others', 'Others'),
    
]