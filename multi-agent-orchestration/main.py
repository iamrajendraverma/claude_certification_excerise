from agents.coordinator import coordinator


def main():
    print("Hello from multi-agent-orchestration!")
    userPromt = "The future of AI in Healthcare"
    report  = coordinator(userPromt)
    print(report.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
