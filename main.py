from datetime import datetime

tasks = []
next_id = 1


def addTask() -> None:
    global next_id

    task = input("\nEnter a task: ")

    if task == "":
        print("\nFAILURE: cannot add an empty task.")
        return

    task_data = {
        "id": next_id,
        "content": task,
        "completed": False,
        "when_created": datetime.now(),
    }

    tasks.append(task_data)
    next_id += 1

    print("\nJust added a task!")
    input("Press any key to continue...")
    print("\n" * 2)


def listTasks() -> None:
    print("\nTasks\n")

    count = 0
    for task in tasks:
        count += 1
        print(
            f"{count}. ID: {task["id"]}. Content: {task["content"]}. When created: {task["when_created"]}. Completed: {"✅" if task["completed"] else "❌"}"
        )

    if count == 0:
        print("No tasks :(")

    print("\nFinished successfully!")
    input("Press any key to continue...")
    print("\n" * 2)


def sortTasks() -> None:
    sort_type = input(
        "\nHow do you want to sort tasks?\n1. Newest\n2. Oldest\n3. Completed\n4. On-going\n>"
    )

    for i in range(len(tasks) - 1):
        for j in range(i, len(tasks)):
            if tasks[i] == tasks[j]:
                continue
            else:
                match (sort_type):
                    case "1":
                        if tasks[i]["when_created"] < tasks[j]["when_created"]:
                            tasks[i], tasks[j] = tasks[j], tasks[i]
                    case "2":
                        if tasks[i]["when_created"] > tasks[j]["when_created"]:
                            tasks[i], tasks[j] = tasks[j], tasks[i]
                    case "3":
                        if not tasks[i]["completed"] and tasks[j]["completed"]:
                            tasks[i], tasks[j] = tasks[j], tasks[i]
                    case "4":
                        if tasks[i]["completed"] and not tasks[j]["completed"]:
                            tasks[i], tasks[j] = tasks[j], tasks[i]

    print("\nSorting is finished!")
    input("Press any key to continue...")
    print("\n" * 2)


def markTaskAsCompleted() -> None:
    try:
        id = int(input("Enter task ID: "))
    except ValueError:
        print("FAILURE: id must be a number.")
        input("Press any key to continue...")
        print("\n" * 2)
        return

    changed = False
    for task in tasks:
        if task["id"] == id:
            task["completed"] = True
            changed = True
            break

    match changed:
        case True:
            print("Successfully marked the task as completed!")
        case False:
            print("Failed to find a task.")

    input("Press any key to continue...")
    print("\n" * 2)


def markTaskAsOnGoing() -> None:
    try:
        id = int(input("Enter task ID: "))
    except ValueError:
        print("FAILURE: id must be a number.")
        input("Press any key to continue...")
        print("\n" * 2)
        return

    changed = False
    for task in tasks:
        if task["id"] == id:
            task["completed"] = False
            changed = True
            break

    match changed:
        case True:
            print("Successfully marked the task as on-going!")
        case False:
            print("Failed to find a task.")

    input("Press any key to continue...")
    print("\n" * 2)


def removeTaskById() -> None:
    try:
        id = int(input("Enter ID: "))
    except ValueError:
        print("FAILURE: id must be a number.")
        input("Press any key to continue...")
        print("\n" * 2)
        return

    i = 0
    found = False
    for task in tasks:
        if task["id"] == id:
            found = True

            # deleting a task
            del tasks[i]

            break
        i += 1

    match found:
        case True:
            print("Successfully deleted a task!")
        case False:
            print("Failed to find a task.")

    input("Press any key to continue...")
    print("\n" * 2)


def main() -> str | None:
    print("\n~~~ TODO APP ~~~\n")

    print("Operations: ")
    choice = input(
        "1. Add task\n2. List tasks\n3. Sort tasks\n4. Mark task as completed\n5. Mark task as on-going\n6. Remove task\n7. Exit\n> "
    )

    match choice:
        case "1":
            addTask()
        case "2":
            listTasks()
        case "3":
            sortTasks()
        case "4":
            markTaskAsCompleted()
        case "5":
            markTaskAsOnGoing()
        case "6":
            removeTaskById()
        case "7":
            return "Cancelled"


if __name__ == "__main__":
    while True:
        result = main()

        match result:
            case "Cancelled":
                print("\nProgram is closed.")
                break
