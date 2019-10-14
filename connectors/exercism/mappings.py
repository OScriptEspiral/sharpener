def get_rust_mappings(prefix, exercise_name, has_hint=False):
    return {
        "readme":f"{prefix}/{exercise_name}/README.md",
        "solution":f"{prefix}/{exercise_name}/example.rs",
        "test":f"{prefix}/{exercise_name}/tests/${exercise_name}.rs",
        "hint":f"{prefix}/{exercise_name}/.meta/hints.md" if has_hint else None,
        "starting_point":f"{prefix}/{exercise_name}/src/lib.rs",
    }
