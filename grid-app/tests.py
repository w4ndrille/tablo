# FILEPATH: /

testCount = 0
testFailCount = 0
debug = False

def runTests():
	global testCount, testFailCount, debug

	debug = False
	debug = True

	testCount = 0
	testFailCount = 0

	# initialize the datastructure for the matrix
	columnCount = 10
	rowCount = 10

	sheetSizes = [{'RowCount': rowCount, 'ColumnCount': columnCount}, {'RowCount': rowCount, 'ColumnCount': columnCount}]

	# For now make this a two way mapping for ordered loops and O(1) access times -- aware of redundancy of state which could cause problems
	sheetNames = {'Sheet1': 0, 'Sheet2': 1}

	sheetList = ['Sheet1', 'Sheet2']

	grid = {'Data': {}, 'PerformanceCounting': {}, 'DirtyCells': {}, 'ActiveSheet': 0, 'SheetNames': sheetNames, 'SheetList': sheetList, 'SheetSizes': sheetSizes}

	if not debug:
		testFormula("((A1 + A10) - (1))", True)
		testFormula("A10 + 0.2", True)
		testFormula("A10 + A0.2", False)
		testFormula("0.1 + 0.2 * 0.3 / 0.1", True)
		testFormula("0.1 + 0.2 * 0.3 / 0.1A", False)
		testFormula("A1 * A20 + 0.2 - \"abc\"", True)
		testFormula("A1 * A + 0.2 - \"abc\"", False)
		testFormula("SUM(A1:10, 10)", False)
		testFormula("A1 ^^ 10", False)
		testFormula("A1 ^ 10", True)
		testFormula("SUM(A1 ^ 10, 1, 1.05))", False)
		testFormula("SUM(A1 ^ 10, 1, 1.05)", True)
		testFormula("SUM(A1 ^ 10, 1, A1.05)", False)
		testFormula("A.01", False)
		testFormula("A10+0.01", True)
		testFormula("A10+A", False)
		testFormula("$A$10+$A1+A$2", True)

		# dollar fixing references
		testFormula("$$A1", False)

		testFormula("Sheet!$A$$1", False)
		testFormula("Sheet!$A$1", True)

		testFormula("Sheet1!$A$$1", False)
		testFormula("Sheet1!$A$1", True)
		testFormula("VLOOKUP(Sheet1!$A$1)", True)
		testFormula("VLOOKUP(A1,Sheet1!$A$1,1)", True)
		testFormula("VLOOKUP(A1,Sheet1!$A$1:$A$1,1)", True)
		testFormula("SUM(Sheet1!$A$1:$A$1)", True)
		testFormula("SUM($A$1:$A$1)", True)
		testFormula("SUM($A$$1:$A$1)", False)
		testFormula("SUM($$A$1:$A$1)", False)
		testFormula("SUM($A$$1:$A$$1)", False)
		testFormula("Sheet1!$A1", True)
		testFormula("Sheet1!A$1", True)
		testFormula("Sheet1!A1", True)
		testFormula("'Sheet 1'!$A$1", True)
		testFormula("'Sheet 1'!$A1", True)
		testFormula("'Sheet 1'!A$1", True)
		testFormula("'Sheet 1'!A1", True)
		testFormula("'Sheet1'!$A$1", True)
		testFormula("'Sheet1'!$A1", True)
		testFormula("'Sheet1'!A$1", True)
		testFormula("'Sheet1'!A1", True)
		testFormula("$A$1", True)
		testFormula("A$1", True)
		testFormula("$A1", True)
		testFormula("A1", True)

		testFormula("A$$1", False)
		testFormula("'0'!A5 + 'Blad 2'!A10 + A10 - Blad15!$A$100", True)
		testFormula("0!A5 + 'Blad 2'!A10 + A10 - Blad15!$A$100", False)
		testFormula("10+-10/10--10", True)
		testFormula("", True)
		testFormula("10+-10/10---10", False)
		testFormula("A10+(-10)", True)
		testFormula("A10+(--10)", False)
		testFormula("A1*-5", True)
		testFormula("*5", False)
		testFormula("$B$1+CEIL(RAND()*1000)", True)

		referenceCount = findReferenceStrings("\"abudh\\\"ijdso\"")
		testBool(len(referenceCount) == 0, True)

		referenceCount2 = findReferenceStrings("\"Then there's a pair of us -- don't tell!\"")
		testBool(len(referenceCount2) == 0, True)

		referenceMap = {'Sheet2!A1': 'Sheet2!A2'}
		testString(replaceReferenceStringInFormula("Sheet2!A1", referenceMap), "Sheet2!A2")

		referenceMap = {"'Sheet 2'!A1": "'Sheet 2'!A2"}
		testString(replaceReferenceStringInFormula("'Sheet 2'!A1", referenceMap), "'Sheet 2'!A2")

		testString(findReferenceStrings("'Sheet  3'!A1")[0], "'Sheet  3'!A1")

		someReferences = findReferenceStrings("'0'!A5 + 'Blad 2'!A10 + A10 - Blad15!$A$100")
		testString(someReferences[0], "'0'!A5")
		testString(someReferences[1], "'Blad 2'!A10")
		testString(someReferences[2], "A10")
		testString(someReferences[3], "Blad15!$A$100")

		print(str(testCount - testFailCount) + "/" + str(testCount) + " tests succeeded. Failed: " + str(testFailCount))

	else:
		# space to run single test cases
		# testFormula("$B$1+CEIL(RAND()*1000)", True)
		# testFormula("'Sheet1'!$A$1", True)
		testFormula("\"Then there's a pair of us -- don't tell!\"", True)

		sampleDv = makeDv("\"Then there's a pair of us -- don't tell!\"")

		resultDv = parse(sampleDv, grid, {'String': "A1", 'SheetIndex': 0})

		print(resultDv['DataString'])

def testString(result, expected):
	global testCount, testFailCount
	testCount += 1
	if result != expected:
		print("[Test #" + str(testCount) + " failed] Expected: " + expected + ", got: " + result)
		testFailCount += 1
	else:
		print("[Test #" + str(testCount) + " succeeded] Got: " + result)

def testBool(result, expected):
	global testCount, testFailCount
	testCount += 1
	if result != expected:
		print("[Test #" + str(testCount) + " failed] Expected: " + str(expected) + ", got: " + str(result))
		testFailCount += 1
	else:
		print("[Test #" + str(testCount) + " succeeded] Expected: " + str(expected) + ", got: " + str(result))

def testFormula(formula, expected):
	global testCount, testFailCount
	testCount += 1
	result = isValidFormula(formula)
	if result != expected:
		print("[Test #" + str(testCount) + " failed] Expected: " + str(expected) + ", got: " + str(result) + " formula: " + formula)
		testFailCount += 1
	else:
		print("[Test #" + str(testCount) + " succeeded] formula: " + formula)