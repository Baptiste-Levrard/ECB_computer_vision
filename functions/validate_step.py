def validate_step(step_name):
    satisfied = input(f"Are you satisfied with the {step_name}? (y/n): ").strip().lower()
    return satisfied == 'y'