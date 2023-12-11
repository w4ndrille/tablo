

def find_max_column_width(column_index, sheet_index, grid, c):
	max_row = grid.SheetSizes[sheet_index].RowCount
	current_row_index = 1

	max_length_found = -1
	max_index_normal_ref = ""
	max_row_index = 1

	while True:
		normal_ref = str(sheet_index) + "!" + indexes_to_reference_string(current_row_index, column_index)
		dv = convert_to_string(get_data_by_normal_ref(normal_ref, grid))

		if len(dv.DataString) > max_length_found:
			max_length_found = len(dv.DataString)
			max_index_normal_ref = normal_ref
			max_row_index = current_row_index

		current_row_index += 1

		if current_row_index > max_row:
			break

	send_cells_by_refs([get_reference_from_map_index(max_index_normal_ref)], grid, c)

	json_data = ["MAXCOLUMNWIDTH", str(max_row_index), str(column_index), str(sheet_index), str(max_length_found)]

	json_data = json.dumps(json_data)

	c.send(json_data)


def find_jump_cell(start_cell, direction, grid, c):
	start_cell_row = get_reference_row_index(start_cell.String)
	start_cell_column = get_reference_column_index(start_cell.String)

	start_cell_empty = is_cell_empty(get_data_from_ref(start_cell, grid))

	horizontal_increment = 0
	vertical_increment = 0

	if direction == "up":
		vertical_increment = -1
	elif direction == "down":
		vertical_increment = 1
	elif direction == "left":
		horizontal_increment = -1
	elif direction == "right":
		horizontal_increment = 1

	current_cell_row = start_cell_row
	current_cell_column = start_cell_column

	is_first_cell_check = True

	while True:
		current_cell_row += vertical_increment
		current_cell_column += horizontal_increment

		if current_cell_row > grid.SheetSizes[grid.ActiveSheet].RowCount or current_cell_row < 1:
			break
		if current_cell_column > grid.SheetSizes[grid.ActiveSheet].ColumnCount or current_cell_column < 1:
			break

		this_cell_empty = is_cell_empty(get_data_from_ref(Reference(String=indexes_to_reference_string(current_cell_row, current_cell_column), SheetIndex=start_cell.SheetIndex), grid))

		if is_first_cell_check and this_cell_empty and not start_cell_empty:
			start_cell_empty = not start_cell_empty

		if not start_cell_empty and this_cell_empty:
			break
		if start_cell_empty and not this_cell_empty:
			current_cell_row += vertical_increment
			current_cell_column += horizontal_increment
			break

		is_first_cell_check = False

	current_cell_row -= vertical_increment
	current_cell_column -= horizontal_increment

	new_cell = indexes_to_reference_string(current_cell_row, current_cell_column)

	json_data = ["JUMPCELL", relative_reference_string(start_cell), direction, new_cell]

	json_data = json.dumps(json_data)

	c.send(json_data)


def get_int_from_string(int_string):
	int_value = int(int_string)
	return int_value


def get_index_from_string(sheet_index_string):
	sheet_index_int = int(sheet_index_string)
	sheet_index = int8(sheet_index_int)
	return sheet_index


def clear_cell(ref, grid):
	dv = get_data_from_ref(ref, grid)

	dv.ValueType = DynamicValueTypeString
	dv.DataFormula = ""
	dv.DataString = ""

	set_data_by_ref(ref, set_dependencies(ref, dv, grid), grid)


def replace_reference_string_in_formula(formula, reference_map):
	if len(reference_map) == 0:
		return formula

	index = 0
	reference_start_index = 0
	reference_end_index = 0
	have_valid_reference = False
	in_quote_section = False
	in_single_quote = False

	while True:
		character = ' '

		if index < len(formula):
			character = formula[index]

		if in_quote_section:
			if character == '"' and formula[index-1] != '\\':
				in_quote_section = False
				reference_start_index = index + 1
				reference_end_index = index + 1
		elif in_single_quote:
			if character == "'":
				in_single_quote = False
			reference_end_index = index
		elif character == '"':
			in_quote_section = True
		elif have_valid_reference:
			if character == ':' or character == '!' or character == "'":
				reference_end_index = index
				have_valid_reference = False
			elif character.isdigit():
				reference_end_index = index
			else:
				left_substring = formula[:reference_start_index]
				right_substring = formula[reference_end_index+1:]

				reference = formula[reference_start_index:reference_end_index+1]

				new_reference = reference

				if reference not in reference_map:
					new_reference = reference_map[reference]

				size_difference = len(new_reference) - len(reference)

				index += size_difference

				formula = left_substring + new_reference + right_substring

				have_valid_reference = False
				reference_start_index = index + 1
				reference_end_index = index + 1
		elif character.isalpha() or character == '$' or character == ':' or character == '!' or character == "'":
			if character == "'":
				in_single_quote = True
			reference_end_index = index + 1
		elif character.isdigit():
			if reference_end_index - reference_start_index > 0:
				reference_end_index = index
				have_valid_reference = True
			else:
				reference_start_index = index + 1
				reference_end_index = index + 1
				have_valid_reference = False
		else:
			reference_start_index = index + 1
			reference_end_index = index + 1
			have_valid_reference = False

		index += 1

		if index >= len(formula) and not have_valid_reference:
			break

	return formula


def replace_references_in_formula(formula, source_index, target_index, reference_map, grid):
	reference_strings = find_reference_strings(formula)

	string_reference_map = {}

	for reference_string in reference_strings:
		if ':' not in reference_string:
			reference = get_reference_from_string(reference_string, source_index, grid)
			string_reference_map[reference_string] = reference_to_relative_string(reference_map[reference], target_index, grid)

	return replace_reference_string_in_formula(formula, string_reference_map)


def replace_reference_ranges_in_formula(formula, source_index, target_index, reference_range_map, grid):
	reference_strings = find_reference_strings(formula)

	string_reference_map = {}

	for reference_string in reference_strings:
		if ':' in reference_string:
			reference_range = get_range_reference_from_string(reference_string, source_index, grid)
			string_reference_map[reference_string] = reference_range_to_relative_string(reference_range_map[reference_range], target_index, grid)

	return replace_reference_string_in_formula(formula, string_reference_map)


def change_sheet_size(new_row_count, new_column_count, sheet_index, c, grid):
	if new_row_count > grid.SheetSizes[sheet_index].RowCount or new_column_count > grid.SheetSizes[sheet_index].ColumnCount:
		for current_column in range(new_column_count + 1):
			for current_row in range(new_row_count + 1):
				if current_column > grid.SheetSizes[sheet_index].ColumnCount or current_row > grid.SheetSizes[sheet_index].RowCount:
					reference = Reference(String=indexes_to_reference_string(current_row, current_column), SheetIndex=sheet_index)

					if not check_data_presence_from_ref(reference, grid):
						set_data_by_ref(reference, make_empty_dv(), grid)

	grid.SheetSizes[sheet_index].RowCount = new_row_count
	grid.SheetSizes[sheet_index].ColumnCount = new_column_count

	send_sheet_size(c, sheet_index, grid)


def insert_row_column(insert_type, direction, reference, c, grid):
	if insert_type == "COLUMN":
		change_sheet_size(grid.SheetSizes[grid.ActiveSheet].RowCount, grid.SheetSizes[grid.ActiveSheet].ColumnCount + 1, grid.ActiveSheet, c, grid)

		base_column = get_reference_column_index(reference)

		if direction == "RIGHT":
			base_column += 1

		maximum_row, maximum_column = determine_minimum_rectangle(1, base_column, grid.ActiveSheet, grid)

		top_left_ref = indexes_to_reference_string(1, base_column)
		bottom_right_ref = indexes_to_reference_string(maximum_row, maximum_column)

		new_top_left_ref = indexes_to_reference_string(1, base_column + 1)
		new_bottom_right_ref = indexes_to_reference_string(maximum_row, maximum_column + 1)

		cut_cells(ReferenceRange(String=top_left_ref + ":" + bottom_right_ref, SheetIndex=grid.ActiveSheet),
				  ReferenceRange(String=new_top_left_ref + ":" + new_bottom_right_ref, SheetIndex=grid.ActiveSheet), grid, c)
	elif insert_type == "ROW":
		change_sheet_size(grid.SheetSizes[grid.ActiveSheet].RowCount + 1, grid.SheetSizes[grid.ActiveSheet].ColumnCount, grid.ActiveSheet, c, grid)

		base_row = get_reference_row_index(reference)

		if direction == "BELOW":
			base_row += 1

		maximum_row, maximum_column = determine_minimum_rectangle(base_row, 1, grid.ActiveSheet, grid)

		top_left_ref = indexes_to_reference_string(base_row, 1)
		bottom_right_ref = indexes_to_reference_string(maximum_row, maximum_column)

		new_top_left_ref = indexes_to_reference_string(base_row + 1, 1)
		new_bottom_right_ref = indexes_to_reference_string(maximum_row + 1, maximum_column)

		cut_cells(ReferenceRange(String=top_left_ref + ":" + bottom_right_ref, SheetIndex=grid.ActiveSheet),
				  ReferenceRange(String=new_top_left_ref + ":" + new_bottom_right_ref, SheetIndex=grid.ActiveSheet), grid, c)


def cut_cells(source_range, destination_range, grid, c):
	source_cells = cell_range_to_cells(source_range)
	destination_cells = copy_source_to_destination(source_range, destination_range, grid, True)

	for ref in source_cells:
		if ref not in destination_cells:
			clear_cell(ref, grid)

	changed_cells = compute_dirty_cells(grid, c)

	return changed_cells