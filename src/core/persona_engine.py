#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoForm Core - Human Persona Simulation Engine
Provides correlated Likert-5 scores, demographic profiles, and realistic answer models.
"""

import random

LIKERT_5_MAP = {
    5: "5 = เห็นด้วยอย่างยิ่ง / สำคัญมากที่สุด",
    4: "4 = เห็นด้วย / สำคัญมาก",
    3: "3 = เห็นด้วยปานกลาง / สำคัญปานกลาง",
    2: "2 = ไม่เห็นด้วย / สำคัญน้อย",
    1: "1 = ไม่เห็นด้วยอย่างยิ่ง / สำคัญน้อยที่สุด"
}

SUSHI_PERSONAS = [
    {
        "name": "Super Fan (Sushi Lover)",
        "weight": 0.55,
        "base_score": 4.85,
        "category_bias": {
            "product": 0.2, "price": -0.1, "place": 0.1, "promo": 0.0,
            "people": 0.15, "process": 0.1, "physical": 0.2, "behavior": 0.25
        }
    },
    {
        "name": "Satisfied Pragmatist",
        "weight": 0.30,
        "base_score": 4.35,
        "category_bias": {
            "product": 0.15, "price": -0.25, "place": 0.0, "promo": -0.1,
            "people": 0.05, "process": 0.05, "physical": 0.1, "behavior": 0.1
        }
    },
    {
        "name": "Value-Conscious Diner",
        "weight": 0.10,
        "base_score": 3.95,
        "category_bias": {
            "product": 0.1, "price": -0.45, "place": -0.1, "promo": 0.2,
            "people": 0.0, "process": -0.1, "physical": 0.05, "behavior": -0.1
        }
    },
    {
        "name": "Critical Quality Inspector",
        "weight": 0.05,
        "base_score": 3.75,
        "category_bias": {
            "product": 0.0, "price": -0.3, "place": 0.0, "promo": -0.2,
            "people": -0.1, "process": -0.2, "physical": 0.1, "behavior": -0.15
        }
    }
]

def generate_sushi_persona_answers(question_categories: dict):
    """
    Generates realistic correlated Likert responses across 7Ps & Behavior
    """
    persona = random.choices(
        SUSHI_PERSONAS,
        weights=[p["weight"] for p in SUSHI_PERSONAS],
        k=1
    )[0]

    respondent_mood = random.gauss(0, 0.12)
    answers = {}

    for q_key, (category, entry_id) in question_categories.items():
        cat_bias = persona["category_bias"].get(category, 0.0)
        raw_score = persona["base_score"] + cat_bias + respondent_mood + random.gauss(0, 0.28)
        score = int(round(max(1, min(5, raw_score))))
        answers[entry_id] = LIKERT_5_MAP[score]

    return answers, persona["name"]
