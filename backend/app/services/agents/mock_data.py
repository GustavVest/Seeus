"""
Mock product fixtures for testing the agent system.

Three example products straight from the product brief:
- Arctic sea mineral supplement entering Japan
- Instant noodle brand entering Germany
- Protein bar entering Korea
"""

from .types import AnalysisInput


ARCTIC_SEA_MINERAL_JP: AnalysisInput = {
    'product_name': 'Arctic Sea Mineral Complex',
    'product_category': 'Supplement',
    'ingredients': [
        'Atlantic sea minerals (magnesium, potassium, calcium)',
        'Marine collagen peptides',
        'Vitamin D3',
        'Natural lemon extract',
    ],
    'claims_on_pack': [
        'Boost daily energy',
        'Natural Arctic minerals',
        'Doctor recommended',
    ],
    'country_of_origin': 'Norway',
    'current_market': 'Norway',
    'target_market': 'Japan',
    'target_channel': 'pharmacy',
    'target_buyer': 'health-conscious',
    'price_tier': 'premium',
    'brand_goal': 'clinical',
}


INSTANT_NOODLE_DE: AnalysisInput = {
    'product_name': 'Quick Bowl Spicy Chicken Ramen',
    'product_category': 'Food',
    'ingredients': [
        'Wheat noodles',
        'Chicken flavor seasoning',
        'Spice blend',
        'Dehydrated vegetables',
        'Soy sauce powder',
    ],
    'claims_on_pack': [
        '100% natural ingredients',
        'No artificial preservatives',
        'Ready in 3 minutes',
    ],
    'country_of_origin': 'South Korea',
    'current_market': 'South Korea',
    'target_market': 'Germany',
    'target_channel': 'supermarket',
    'target_buyer': 'mass',
    'price_tier': 'mainstream',
    'brand_goal': 'fun',
}


PROTEIN_BAR_KR: AnalysisInput = {
    'product_name': 'Forge Protein Bar — Salted Caramel',
    'product_category': 'Food',
    'ingredients': [
        'Whey protein isolate',
        'Almonds',
        'Dates',
        'Cocoa',
        'Natural caramel flavor',
        'Sea salt',
    ],
    'claims_on_pack': [
        '20g protein',
        'Clinically proven recovery',
        'Clean ingredients',
    ],
    'country_of_origin': 'USA',
    'current_market': 'USA',
    'target_market': 'South Korea',
    'target_channel': 'amazon',
    'target_buyer': 'gen-z',
    'price_tier': 'premium',
    'brand_goal': 'functional',
}


EXAMPLES = {
    'arctic_jp': ARCTIC_SEA_MINERAL_JP,
    'noodle_de': INSTANT_NOODLE_DE,
    'protein_kr': PROTEIN_BAR_KR,
}
