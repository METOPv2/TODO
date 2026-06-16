tasks = []


def addTask() -> None:
    global tasks

    task = input("\nEnter a task: ")

    if task == "":
        print("\nFAILURE: cannot add an empty task.")
        return

    task_data = {
        "id": len(tasks) + 1,
        "content": task,
        "completed": False,
    }

    tasks += [task_data]
    print("\nJust added a task!")
    input("Press any key to conitnue...")
    print("\n" * 2)


def listTasks() -> None:
    print("\nTasks\n")

    i = 0
    for task in tasks:
        i += 1
        print(
            f"{i}. ID: {task["id"]}. Content: {task["content"]}. Completed: {"✅" if task["completed"] else "❌"}"
        )

    if i == 0:
        print("No tasks :(")

    print("\nFinished successfully!")
    input("Press any key to continue...")
    print("\n" * 2)


def completeTask() -> None:
    id = int(input("Enter task ID: "))

    if not id:
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
            print("Successfully changed a task!")
        case False:
            print("Failed to find a task.")

    input("Press any key to continue...")
    print("\n" * 2)


def removeTaskById() -> None:
    id = int(input("Enter ID: "))

    if not id:
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
        "1. Add task\n2. List tasks\n3. Complete task\n4. Remove task\n5. Exit\n> "
    )

    match choice:
        case "1":
            addTask()
        case "2":
            listTasks()
        case "3":
            completeTask()
        case "4":
            removeTaskById()
        case "5":
            return "Cancelled"


if __name__ == "__main__":
    while True:
        result = main()

        match result:
            case "Cancelled":
                print("\nProgram is closed.")
                break
