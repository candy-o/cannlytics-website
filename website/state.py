"""
State Variables | Cannlytics Website
Copyright (c) 2021 Cannlytics

Authors: Keegan Skeate <keegan@cannlytics.com>
Created: 10/15/2020
Updated: 11/28/2021
License: MIT License <https://github.com/cannlytics/cannlytics-website/blob/main/LICENSE>
"""

# Page-specific Firestore documents and collections.
page_data = {
    "contact": {
        "documents": [{"name": "recaptcha", "ref": "admin/recaptcha"}]
    },
    "contributors": {
        "collections": [{"name": "contributors", "ref": "public/contributors/contributor_data"}],
    },
    "market": {
        "collections": [
            {
                "name": "datasets",
                "ref": "public/market/datasets",
                "limit": 10,
                "order_by": "published_at",
                "desc": True
            }
        ],
    },
    "events": {
        "collections": [{"name": "events", "ref": "public/events/event_data"}],
    },
    "homepage": {
        "collections": [
            {
                "name": "video_archive",
                "ref": "public/videos/video_data",
                "limit": 3,
                "order_by": "published_at",
                "desc": True
            },
            {
                "name": "verifications",
                "ref": "public/verifications/verification_data",
                "limit": None,
                "order_by": "state",
            },
        ],
    },
    "partners": {
        "collections": [{"name": "partners_list", "ref": "public/partners/partner_data"}],
    },
    "team": {
        "collections": [{"name": "team", "ref": "public/team/team_members"}],
    },
    "videos": {
        "collections": [
            {
                "name": "video_archive",
                "ref": "public/videos/video_data",
                "limit": 10,
                "order_by": "published_at",
                "desc": True
            }
        ],
    },
    "whitepapers": {
        "collections": [{"name": "whitepapers", "ref": "public/whitepapers/whitepaper_data"}],
    }
}

# Page-specific markdown documents.
page_docs = {
    "about": ["about"],
    "contributors": ["contribute"],
}

# Page-specific context.
state = {
    "account": {
         "user_fields": [
            {"key": "name", "label": "Name"},
            # {"key": "position", "label": "Position"},
            {"type": "email", "key": "email", "label": "Email"},
            {"key": "phone_number", "label": "Phone"},
        ],
        "user_options": [
            {
                "title": "Change your password",
                "url": "/account/password-reset",
            },
            {
                "title": "Manage your subscription",
                "url": "/account/subscription",
            },
            {
                "title": "Make a suggestion",
                "url": "/account/feedback",
            },
        ],
    },
    "contact": {
        "title": "Contact Us",
        "message": "You're welcome to contact us anytime about anything. Please enter your contact information and message and the team will get back to you as soon as possible.",
    },
    "general": {
        "title": "Cannlytics",
        "blurb": "Cannlytics is a suite of free software for cannabis-testing laboratories, empowering you with a state-of-the-art system.",
        "email": "contact@cannlytics.com",
        "phone": "(828) 395-3954",
        "phone_number": "18283953954",
        "social": [
            {
                "title": "GitHub",
                "url": "https://github.com/cannlytics"
            },
            {
                "title": "LinkedIn",
                "url": "https://linkedin.com/company/cannlytics"
            },
        ]
    },
    "header": {
        "action": {
            "title": "Download",
            "url": "download"
        },
        "links": [
            {
                "slug": "community",
                "title": "Community"
            },
            {
                "slug": "posts",
                "title": "Docs"
            },
            {
                "slug": "contact",
                "title": "Contact"
            },
        ]
    },
    "homepage": {
        "hero": {
            "title": "Cannabis Analytics for the 21st Century",
            "message": "Get superpowers with open-source cannabis analytics made with love ❤️‍🔥!",
            "image": "website/images/engine_icons/space_station.svg",
            "primary_action": "Get Started 🌱",
            "primary_action_url": "https://docs.cannlytics.com",
            "secondary_action": "Sign Up 🚀",
            "secondary_action_url": "https://console.cannlytics.com",
        },
        "features": [
            {
                "title": "Smart Integrations",
                "message": "We believe that everyone benefits when people are able to study and tinker with their software. With the freedom provided by Cannlytics, users control their software and what it does for them.",
                "image": "website/images/illustrations/outline/lab_tablet.svg",
                "action": "View options",
                "action_url": "/support",
            },
            {
                "title": "Analysis Tailored",
                "message": "Cannlytics provides a user-friendly interface to quickly receive samples, perform analyses, collect and review results, and publish certificates of analysis (CoAs). There are also built in logistics, CRM (client relationship management), inventory management, and invoicing tools.",
                "image": "website/images/illustrations/outline/lab_microscope.svg",
                "action": "Contribute now",
                "action_url": "/community",
                "action": "Begin customizing",
                "action_url": "https://console.cannlytics.com",
            },
            {
                "title": "Community Driven", # vs. People Centric (AB TEST)
                "message": "Built by scientist for scientists. Cannlytics empowers you with control over the development process, resources, and decision making authority. We believe that the Cannlytics community is the best judge of how Cannlytics can be improved, so, we have entrusted Cannlytics' source code with you.",
                "image": "website/images/illustrations/outline/lab_microbiologist.svg",
                "action": "Contribute now",
                "action_url": "/community",
            }
        ],
        "featurettes": [
            {
                "title": "Automate your lab.",
                "subtitle": "Free your time for science and analysis.",
                "message": "The more mundane tasks that you can automate and execute quickly and efficiently with the Cannlytics Engine, then the more time you have to conduct science and experiments.",
                "image": "website/images/screenshots/console_intake_light.png",
                "image_dark": "website/images/screenshots/console_intake_dark.png",
            },
            {
                "title": "Extend, modify, and personalize.",
                "subtitle": "Add anything that you need.",
                "message": "An advantage of the Cannlytics Engine over proprietary software solutions is that Cannlytics lets you make modifications as you need because Cannlytics is an open box of free software.",
                "image": "website/images/screenshots/console_account_light.png",
                "image_dark": "website/images/screenshots/console_account_dark.png",
            },
            {
                "title": "Freedom at your fingertips.",
                "subtitle": "It's all yours.",
                "message": "Cannlytics is a system of free software that you can use to power your lab. Cannlytics belongs to you so that you can use the Cannlytics Engine however that you please. Free software lets you operate ethically with the sky as the limit.",
                "image": "website/images/screenshots/console_help_light.png",
                "image_dark": "website/images/screenshots/console_help_dark.png",
            }
        ]
    },
    "support": {
        "pricing_tiers": [
            {
                "name": "Free",
                "price": "👐",
                "color": "green",
                "action": "Sign up for free",
                "url": "https://console.cannlytics.com",
                "attributes": [
                    "All software",
                    "All community material",
                    "GitHub Issues",
                    "Email support",
                ],
            },
            {
                "name": "Premium",
                "price": "$500 / mo.",
                "color": "orange",
                "action": "Get started",
                "url": "/subscriptions/checkout/?name=Premium",
                "attributes": [
                    "Metrc integration",
                    "Access to development builds",
                    "Priority GitHub Issues",
                    "Remote support",
                ],
            },
            {
                "name": "Enterprise",
                "price": "$2000 / mo.",
                "color": "purple",
                "action": "Contact us",
                "url": "/subscriptions/checkout/?name=Enterprise",
                "attributes": [
                    "Custom installation",
                    "Access to internal tools",
                    "Early access to new features",
                    "3 on-site support days / year",
                ],
            },
        ],
    },
    "partners": {
        "fields": [
            {"type": "email", "key": "email", "title": "Email"},
            {"type": "text", "key": "name", "title": "Name"},
            {"type": "text", "key": "twitter", "title": "Twitter", "group": "@"},
            {"type": "text", "key": "linkedin", "title": "LinkedIn"},
            {"type": "text", "key": "position", "title": "Position"},
            {"type": "text", "key": "location", "title": "Location"},
        ],
    },
    "footer": {
        "index": [
            {
                "name": "Community",
                "links": [
                    {"title": "Labs", "page": "community"},
                    {"title": "Producers", "page": "producers"},
                    {"title": "Retailers", "page": "retailers"},
                    {"title": "Integrators", "page": "integrators"},
                    {"title": "Data Scientists", "page": "data-science"},
                ]
            },
            {
                "name": "Docs",
                "links": [
                    {"title": "API", "url": "https://docs.cannlytics.com/api/about"},
                    {"title": "Developers", "url": "https://docs.cannlytics.com/developers/development"},
                    {"title": "LIMS", "url": "https://docs.cannlytics.com/cannlytics/lims/lims"},
                    {"title": "Metrc", "url": "https://docs.cannlytics.com/cannlytics/traceability/metrc"},
                    {"title": "Users", "url": "https://docs.cannlytics.com/console/get-started"},
                ]
            },
            {
                "name": "About",
                "links": [
                    {"title": "Story", "url": "https://docs.cannlytics.com/about/about"},
                    {"title": "Roadmap", "url": "https://docs.cannlytics.com/developers/roadmap"},
                    {"title": "Whitepapers", "page": "whitepapers"},
                    {"title": "Donations", "url": "https://opencollective.com/cannlytics-company"},
                    {"title": "Support", "page": "support"},
                ]
            }
        ]
    },
}

# Context for lab pages.
lab_state = {
    "detail_fields": [
        {"key": "name", "title": "Name", "type": "text"},
        {"key": "trade_name", "title": "Trade name", "type": "text"},
        {"key": "phone", "title": "Phone", "type": "text"},
        {"key": "email", "title": "Email", "type": "email"},
        {"key": "website", "title": "Website", "type": "text"},
        {"key": "linkedin", "title": "LinkedIn", "type": "text"},
        {"key": "street", "title": "Street", "type": "text"},
        {"key": "city", "title": "City", "type": "text"},
        {"key": "county", "title": "County", "type": "text"},
        {"key": "state", "title": "State", "type": "text"},
        {"key": "zip", "title": "Zip", "type": "text"},
        {"key": "latitude", "title": "Latitude", "type": "number"},
        {"key": "longitude", "title": "Longitude", "type": "number"},
        {"key": "license", "title": "License", "type": "text"},
        {"key": "license_url", "title": "License URL", "type": "text"},
        {"key": "status", "title": "License status", "type": "text"},
        {"key": "capacity", "title": "Capacity", "type": "text"},
        {"key": "square_feet", "title": "Square Feet", "type": "text"},
        {"key": "brand_color", "title": "Brand color", "type": "color"},
        {"key": "secondary_color", "title": "Secondary color", "type": "color"},
        {"key": "favicon", "title": "Icon URL", "type": "textarea"},
        {"key": "image_url", "title": "Image URL", "type": "textarea"},
        # TODO: Keep track of certifications
        # - dea_licensed_hemp_lab
        # - a2la_certified
    ],
    "tabs": [
        {"name": "Details", "section": "details", "active": "true"},
        {"name": "Analyses", "section": "analyses"},
        {"name": "Change log", "section": "logs"},
    ]
}
