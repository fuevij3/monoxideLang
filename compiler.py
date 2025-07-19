import math

mem = []
allocated = 1024  # pre-allocate 1 KB

def compiler(code):
    counter = 0
    for i in code:
        counter += 1

        if i.startswith("echo"):
            args = i.split("::")
            for i in range(1, len(args)):
                print(args[i])
        # directly prints the inputted string

        # mem class
        elif i.startswith("mem"):
            types = i.split(".")
            if types[1] == "alloc":
                arg = i.split("::")
                allocated = int(arg[1])
            # sets mem limit
            elif types[1] == "read":
                arg = i.split("::")
                block = mem[int(arg[1])]
                if block["type"] == "var":
                    label = block["varLabel"]
                    value = block["varValue"]
                    print("varLabel:", label, "varValue:", value)

            # reads directly from mem
            elif types[1] == "add":
                args = i.split("::")
                addr = int(args[1])
                value = args[2]
                block_size = len(value)
                mem_size = sum(len(str(b)) for b in mem)

                if mem_size + block_size < allocated:
                    mem.insert(addr, value)
                else:
                    print("mem_overflow::error01")


            # adds directly to mem using an address and value
            elif types[1] == "del":
                arg = i.split("::")
                if int(arg[1]) <= len(mem):
                    mem.pop(int(arg[1]))
                else:
                    print("mem_outofbounds::error02")

            # deletes from mem

        elif i.startswith("print"):
            args = i.split("::")
            block_type = args[1]
            block_label = args[2]
            if block_type == "var":
                for i in mem:
                    if i["type"] == "var":
                        print(i["varValue"])

        elif i.startswith("var"):
            args = i.split("::")
            args2 = i.split("=")
            info = {
                "type": "var",
                "varLabel": args[1],
                "varValue": args2[1]
            }

            mem.append(info)

        # arith class
        elif i.startswith("arith"):
            command_part = i.split("::")[0]  # arith.add
            type_and_args = i.split("::")[1]  # int(3,5)

            operation = command_part.split(".")[1]
            value_type = type_and_args.split("(")[0]
            raw_args = type_and_args.split("(")[1].replace(")", "")
            args = raw_args.split(",")

            if value_type == "int":
                a = int(args[0])
                b = int(args[1]) if len(args) > 1 else None

            elif value_type == "var":
                a = b = None
                for block in mem:
                    if block.get("type") == "var":
                        if block.get("varLabel") == args[0]:
                            a = int(block["varValue"])
                        if block.get("varLabel") == args[1]:
                            b = int(block["varValue"])
                if a is None or b is None:
                    print("var_not_found::error03")
                    continue

            result = None
            if operation == "add":
                result = a + b
            elif operation == "subt":
                result = a - b
            elif operation == "div":
                result = a / b
            elif operation == "mult":
                result = a * b
            elif operation == "cosin":
                result = math.cos(a)
            elif operation == "sin":
                result = math.sin(a)
            elif operation == "sqrt":
                result = math.sqrt(a)
            elif operation == "round":
                if b is not None:
                    result = round(a, b)
                else:
                    result = round(a)
            elif operation == "pow":
                if b is not None:
                    result = a ** b
                else:
                    result = a * a

            if result is not None:
                mem.append({"type": "temp", "value": result})

        # stack
        elif i.startswith("stack"):
            args = i.split(".")
            if args[1] == "new":
                name = i.split("::")
                info = {
                    "type": "stack",
                    "name": name[1],
                    "value": []
                }
                mem.append(info)
            elif args[1] == "insert":
                args1 = i.split("::")

                arr = args1[1]
                value = args[2]

                for i in mem:
                    if i["type"] == "stack" and i["name"] == arr:
                        i["value"].append(value)
            elif args[1] == "pop":
                args1 = i.split("::")

                arr = args1[1]

                for i in mem:
                    if i["type"] == "stack" and i["name"] == arr:
                        if len(i["value"]) != 0:
                            i["value"].pop()
                        else:
                            print("nothing_to_pop::error03")
            elif args[1] == "peek":
                args1 = i.split("::")
                arr = args[1]
                for i in mem:
                    if i["type"] == "stack" and i["name"] == arr:
                        if len(i["value"]) != 0:
                            stack = i["value"]
                            mem.append(stack[len(stack) - 1])

        elif i.startswith("file"):
            args = i.split(".")
            if args[1] == "new":
                args1 = i.split("::")
                with open(args1[1], "w") as file:
                    file.write(args1[2])

            elif args[1] == "read":
                args1 = i.split("::")
                mem_size = sum(len(str(b)) for b in mem)
                with open(args1[1], "r") as file:
                    block = file.read(args1[2])
                    if mem_size + len(block) < allocated:
                        mem.append(block)
                    else:
                        print("mem_overflow::error01")


            elif args[1] == "append":
                args1 = i.split("::")
                with open(args1[1], "a") as file:
                    file.write(args1[2])