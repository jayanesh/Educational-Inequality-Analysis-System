from django.core.management.base import BaseCommand
from analytics_dashboard.db_utils import get_school_data_collection
import random

class Command(BaseCommand):
    help = 'Seeds MongoDB with sample education data'

    def handle(self, *args, **options):
        collection = get_school_data_collection()
        collection.delete_many({}) # Clear existing

        states = ["Bihar", "Uttar Pradesh", "Kerala", "Tamil Nadu", "Rajasthan", "Maharashtra", "West Bengal", "Gujarat"]
        years = [2020, 2021, 2022, 2023, 2024]
        levels = ["Primary", "Upper Primary", "Secondary", "Higher Secondary"]
        genders = ["Male", "Female", "Total"]
        categories = ["General", "SC", "ST", "OBC"]

        records = []
        for state in states:
            # Baseline factors per state
            base_poverty = random.uniform(10, 40)
            base_infra = random.uniform(50, 90)
            base_lit = random.uniform(60, 95)
            
            for year in years:
                # Improving trends
                infra = min(100, base_infra + (year - 2020) * 2)
                lit = min(100, base_lit + (year - 2020) * 1.5)
                poverty = max(5, base_poverty - (year - 2020) * 1.2)
                
                for level in levels:
                    for cat in categories:
                        for gender in genders:
                            # Higher levels, specific categories often have higher dropout
                            cat_modifier = 1.5 if cat in ["SC", "ST"] else 1.0
                            level_modifier = 2.0 if level in ["Secondary", "Higher Secondary"] else 1.0
                            
                            # Dropout rates usually higher in poorer states
                            dropout = max(0.5, (poverty / 5) * cat_modifier * level_modifier * random.uniform(0.8, 1.2))
                            
                            records.append({
                                "state": state,
                                "district": f"{state}_District_{random.randint(1,5)}",
                                "year": year,
                                "school_level": level,
                                "gender": gender,
                                "social_category": cat,
                                "dropout_rate": round(dropout, 2),
                                "infrastructure_index": round(infra, 2),
                                "poverty_ratio": round(poverty, 2),
                                "literacy_rate": round(lit, 2),
                                "pupil_teacher_ratio": round(random.uniform(20, 50), 1)
                            })
        
        collection.insert_many(records)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(records)} records into MongoDB'))
