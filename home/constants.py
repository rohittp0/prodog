class RequestType:
    choice_names = [
        "General Maintenance",
        "Electrical",
        "Plumbing",
        "HVAC",
        "Landscaping",
        "Pest Control",
        "Cleaning",
        "Security",
        "Other"
    ]

    @classmethod
    def length(cls):
        return max(len(choice) for choice in cls.choice_names)

    @classmethod
    def choices(cls):
        return [(choice, choice.lower()) for choice in cls.choice_names]


class Status:
    choice_names = [
        "Pending",
        "In Progress",
        "Completed",
        "On Hold",
        "Cancelled"
    ]

    @classmethod
    def length(cls):
        return max(len(choice) for choice in cls.choice_names)

    @classmethod
    def choices(cls):
        return [(choice.lower(), choice) for choice in cls.choice_names]

    @classmethod
    def default(cls):
        return cls.choices()[0][0]
