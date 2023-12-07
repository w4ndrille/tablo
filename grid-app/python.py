import sys
import json

def stream_python_e_out(stdout_pipe, python_in, c, close_channel):
	buffer = bytearray(100)
	buffer_string = ""

	while True:
		command = close_channel.get()
		if command == "CLOSE":
			return

		try:
			n = stdout_pipe.readinto(buffer)
		except Exception as e:
			print(e)
			continue

		if n == 0:
			stdout_pipe.close()
			return

		buffer_string += buffer[:n].decode()

		if buffer_string.endswith("\n"):
			error_string = buffer_string

			json_data = ["INTERPRETER"]
			json_data.append("[error]" + error_string)
			json_string = json.dumps(json_data)
			c.send(json_string)

			json_data2 = ["COMMANDCOMPLETE"]
			json_string2 = json.dumps(json_data2)
			c.send(json_string2)

			buffer_string = ""

def stream_python_out(stdout_pipe, python_in, c, close_channel):
	buffer = bytearray(32768)
	buffer_holder = bytearray()

	while True:
		command = close_channel.get()
		if command == "CLOSE":
			return

		while True:
			try:
				n = stdout_pipe.readinto(buffer)
			except Exception as e:
				print(e)
				continue

			if n == 0:
				stdout_pipe.close()
				return

			if n != len(buffer):
				sub_buffer = buffer[:n]
				buffer_holder.extend(sub_buffer)

				parse_python_output(buffer_holder, python_in, c)

				buffer_holder.clear()
			else:
				buffer_holder.extend(buffer)

def parse_python_output(buffer_holder, python_in, c):
	if buffer_holder.endswith(b"#ENDPARSE#"):
		parse_strings = buffer_holder.decode().split("#ENDPARSE#")

		for e in parse_strings:
			if len(e) > 0:
				new_string = e

				if len(new_string) > 16 and new_string[:17] == "#COMMANDCOMPLETE#":
					json_data = ["COMMANDCOMPLETE"]
					json_string = json.dumps(json_data)
					c.send(json_string)

				elif len(new_string) > 6 and new_string[:7] == "#PARSE#":
					c.actions.append(new_string[7:].encode())

				elif len(new_string) > 6 and new_string[:7] == "#IMAGE#":
					commands = new_string.split("#IMAGE#")[1:2]
					for command in commands:
						c.send(command.encode())

				elif len(new_string) > 15 and new_string[:16] == "#PYTHONFUNCTION#":
					commands = new_string.split("#PYTHONFUNCTION#")[1:2]
					c.grid.python_result_channel.append(commands[0])

				elif len(new_string) > 5 and new_string[:6] == "#DATA#":
					cell_range_string = new_string[6:]
					cells = get_reference_range_from_map_index(cell_range_string)
					command_buf = []

					for e in cells:
						value_dv = get_data_from_ref(e, c.grid)
						value = convert_to_string(value_dv).data_string

						command = f"sheet_data[\"{get_map_index_from_reference(e)}\"] = "
						if value_dv.value_type == DynamicValueTypeString:
							command += f"\"{value.replace('\"', '\\\"')}\""
						else:
							command += f"\"\" if len({value}) == 0 else {value}"

						command_buf.append(command)

					command_buf.append("")
					python_in.write("\n".join(command_buf).encode())

				elif len(new_string) > 12 and new_string[:13] == "#INTERPRETER#":
					json_data = ["INTERPRETER"]
					json_data.append(new_string[13:])
					json_string = json.dumps(json_data)
					c.send(json_string)

def python_interpreter(c):
	python_command = "python3.7" if sys.platform != "win32" else "python"
	python_cmd = subprocess.Popen([python_command, "-u", "python/init.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	close_channel = queue.Queue()

	python_out_thread = threading.Thread(target=stream_python_out, args=(python_cmd.stdout, python_cmd.stdin, c, close_channel))
	python_e_out_thread = threading.Thread(target=stream_python_e_out, args=(python_cmd.stderr, python_cmd.stdin, c, close_channel))

	python_out_thread.start()
	python_e_out_thread.start()

	while True:
		command = c.commands.get()

		if command == "CLOSE":
			close_channel.put("CLOSE")
			return

		python_cmd.stdin.write((command + "\n\n").encode())
		python_cmd.stdin.flush()