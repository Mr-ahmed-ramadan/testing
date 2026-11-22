"""Builds the learning-objective inventory (objectives.json / objectives.csv).

Row format: (id, objective, visual_model, mastery_check, prerequisites, tag)
  id      -> STRAND + STAGE + "." + n   e.g. AS1.5 = Addition/Subtraction, Stage 1, item 5
  tag     -> ""      core England National Curriculum content for that year
             "T:xx"  core AND directly assessed in a statutory/key test (xx = test)
             "P:xx"  beyond the England curriculum at this stage, borrowed from xx
                     (JP Japan, SG Singapore, FI Finland, R research evidence)
"""
import csv, json, re, pathlib
from animations import SCENES, ANIM

STAGES = {
    0: ("Stage 0", "Reception", "4-5"),
    1: ("Stage 1", "Year 1", "5-6"),
    2: ("Stage 2", "Year 2", "6-7"),
    3: ("Stage 3", "Year 3", "7-8"),
    4: ("Stage 4", "Year 4", "8-9"),
    5: ("Stage 5", "Year 5", "9-10"),
    6: ("Stage 6", "Year 6", "10-11"),
    7: ("Stage 7", "Year 7 (KS3)", "11-12"),
    8: ("Stage 8", "Year 8 (KS3)", "12-13"),
    9: ("Stage 9", "Year 9 (KS3)", "13-14"),
    10: ("Stage 10", "GCSE Foundation (Y10-11)", "14-16"),
    11: ("Stage 11", "GCSE Higher only (Y10-11)", "14-16"),
}
STRANDS = {
    "NS": "Number sense & place value",
    "AS": "Addition & subtraction",
    "MD": "Multiplication & division",
    "FR": "Fractions, decimals & percentages",
    "RP": "Ratio & proportion",
    "AL": "Algebra & pattern",
    "ME": "Measurement, money & time",
    "GE": "Geometry & spatial reasoning",
    "ST": "Statistics",
    "PB": "Probability",
    "PS": "Reasoning & problem solving",
}
TESTS = {
    "RBA": "Reception Baseline Assessment",
    "ELG": "EYFS Early Learning Goal (end of Reception)",
    "MTC": "Multiplication Tables Check (Year 4, June)",
    "SATs": "KS2 SATs (Year 6, May)",
    "GCSE": "GCSE Mathematics",
}

R = [
# ---------------- STAGE 0 · Reception ----------------
("NS0.1","Subitise up to 5: see how many dots, fingers or objects there are without counting","Dot cards, dice faces, five-frame flashes","Flash 4 dots for 1 second; child says 4 without counting",[],"T:ELG"),
("NS0.2","Count objects one-to-one up to 10 and know the last number said tells how many (cardinality)","Counters moved one at a time into a line","After counting 8 bears, answers 'how many?' with 8 without recounting",[],"T:RBA"),
("NS0.3","Say the counting sequence to 20 and beyond; start counting from a number other than 1","Number track, counting songs","Counts on from 6 to 15 without restarting at 1",[],"T:ELG"),
("NS0.4","Recognise numerals 0-10 and match each to a quantity","Numeral cards beside dot sets","Matches 7 to a set of seven objects",["NS0.2"],"T:RBA"),
("NS0.5","Compare two groups up to 10: more, fewer, the same, by matching as well as counting","Two rows of counters lined up side by side","Says which row has more when one row is spread out wider",["NS0.2"],"T:ELG"),
("NS0.6","Find one more and one less than a number to 10","Number track, staircase of cubes","Says one less than 7 is 6 instantly",["NS0.3"],""),
("NS0.7","Understand that a quantity stays the same when it is moved or spread out (conservation)","Counters rearranged in front of the child","Knows 6 counters in a circle is still 6 without recounting",["NS0.2"],"P:R"),
("AS0.1","See numbers to 5 as made of smaller parts (part-whole): 5 is 4 and 1, 3 and 2","Part-whole diagram, five-frame, fingers","Shows 5 as two parts in two different ways",["NS0.1"],"T:ELG"),
("AS0.2","Recall number bonds to 5 automatically","Five-frame, hands behind back game","Answers 'I have 2, how many more to make 5?' within 3 seconds",["AS0.1"],"T:ELG"),
("AS0.3","Recall some bonds to 10, including doubles to 5+5","Ten-frame, Numicon-style shapes, domino doubles","Knows double 4 is 8 without counting",["AS0.2"],"T:ELG"),
("AS0.4","Act out adding to and taking away from small groups in stories","Toy figures, story mats","Solves '3 ducks, 2 more come, how many?' with objects",["NS0.2"],""),
("MD0.1","Share objects fairly into equal groups and spot when a share is unfair","Plates and sweets, sharing circles","Shares 6 grapes between 2 plates and checks they are fair",["NS0.2"],"T:ELG"),
("MD0.2","Explore odd and even by pairing objects","Pairs of socks, two-row ten-frames","Says 7 cubes cannot all be paired up",["NS0.2"],"T:ELG"),
("AL0.1","Copy, continue and create repeating patterns (ABAB, ABB, ABC)","Beads, coloured cubes, claps","Continues red-red-blue three more times",[],""),
("GE0.1","Name and describe familiar 2D and 3D shapes; build pictures from shapes","Pattern blocks, tangram pieces, junk modelling","Makes a house from a square and a triangle",[],""),
("GE0.2","Use position words: in front, behind, on top, under, next to, between","Hide-and-find games, Bee-Bot style floor robot","Places a toy between two others on instruction",[],""),
("ME0.1","Compare length, weight and capacity directly: longer, heavier, holds more","Balance scale, cups of water, ribbons","Uses a balance to say which of two objects is heavier",[],""),
("ME0.2","Sequence daily events with before, after, first, then, next","Picture cards of the day","Orders four routine pictures correctly",[],""),
("PS0.1","Explain an idea in their own words when asked 'how do you know?'","Talk prompts, show-me with objects","Gives a reason, not just an answer",[],""),

# ---------------- STAGE 1 · Year 1 ----------------
("NS1.1","Count to and across 100, forwards and backwards, from any number","Hundred square, bead string","Counts back from 63 to 48 without slips",["NS0.3"],""),
("NS1.2","Count in 2s, 5s and 10s","Hands (5s), pairs of shoes (2s), ten-frames (10s)","Counts in 5s to 50 and back",["NS1.1"],""),
("NS1.3","Read and write numerals to 100 and number words to 20","Numeral and word cards","Writes 'fifteen' and 15",["NS0.4"],""),
("NS1.4","See teen numbers as ten and some more (13 = 10 + 3)","Full ten-frame plus loose counters, rekenrek","Builds 16 as a full ten and 6 without counting in ones",["NS1.7"],""),
("NS1.5","Find one more and one less than any number to 100","Hundred square","Says one less than 70 is 69",["NS0.6","NS1.1"],""),
("NS1.6","Show numbers with objects and on a number line; use equal to, more than, less than, most, least","Number line, cubes","Places 12 and 17 on a 0-20 line and says which is more",["NS1.4"],""),
("NS1.7","Subitise structured quantities up to 10 (ten-frame, dice, finger patterns)","Ten-frame flashes, rekenrek","Says 7 from a 1-second ten-frame flash",["NS0.1"],"P:JP"),
("AS1.1","Know all number bonds to 10 fluently, in both orders","Ten-frame, part-whole model, bonds rainbow","Answers 10 = 6 + ? within 3 seconds, for every pair",["AS0.3"],""),
("AS1.2","Know and derive number bonds within 20 (14 = 9 + 5)","Two ten-frames, rekenrek","Explains 9 + 5 using a known fact",["AS1.1","NS1.4"],""),
("AS1.3","Read, write and interpret statements using +, - and =","Number sentences matched to pictures","Writes a number sentence for a picture story",["AS0.4"],""),
("AS1.4","Add and subtract one-digit and two-digit numbers within 20, including zero","Number line jumps, cubes","Solves 15 - 7 with a strategy, not counting all",["AS1.2"],""),
("AS1.5","Use the make-ten strategy to add across 10 (8 + 5 = 8 + 2 + 3)","Two ten-frames, cherry split diagram (Japanese sakuranbo keisan)","Explains 9 + 4 by moving 1 to make 10",["AS1.1","NS1.4"],"P:JP"),
("AS1.6","Subtract back through 10 (13 - 5 = 13 - 3 - 2) or from 10 (13 - 5 = 10 - 5 + 3)","Ten-frames, number line","Solves 14 - 6 by splitting the 6",["AS1.5"],"P:JP"),
("AS1.7","Solve missing-number problems such as 7 = ? - 9","Part-whole model, balance","Finds the missing number in ? + 4 = 11",["AS1.3"],""),
("AS1.8","Understand = as 'has the same value as', not 'the answer comes next'","Balance scale, equations written both ways round","Agrees that 8 = 5 + 3 and 4 + 4 = 5 + 3 are true",["AS1.3"],"P:R"),
("AS1.9","Solve one-step word problems by drawing them, including a simple bar model","Bar model (Singapore), sketches","Draws a bar for 'Sam has 6, Ali has 3 more'",["AS1.4"],"P:SG"),
("MD1.1","Solve one-step multiplication and division problems using objects, pictures and arrays","Arrays of counters, egg boxes","Makes 3 groups of 4 and finds the total",["NS1.2"],""),
("MD1.2","Double and halve numbers to 20","Mirror, ten-frames","Knows double 7 and half of 14",["AS0.3"],""),
("FR1.1","Recognise a half as one of two equal parts of a shape, object or quantity","Folding paper, sharing counters","Says whether a shape is cut into halves or not",["MD0.1"],""),
("FR1.2","Recognise a quarter as one of four equal parts","Folding paper, pizza pictures","Finds a quarter of 8 counters",["FR1.1"],""),
("ME1.1","Compare, describe and measure length, mass, capacity and time, starting with non-standard units","Cubes, hand spans, balance","Measures a book in cubes and compares two books",["ME0.1"],""),
("ME1.2","Recognise UK coins and notes and their values","Real or play coins","Picks out the 20p coin",[],""),
("ME1.3","Know days of the week, months and seasons; sequence events","Calendar, picture timeline","Names the day after Thursday",["ME0.2"],""),
("ME1.4","Tell the time to the hour and half past; draw the hands","Geared clock","Sets a clock to half past 3",["ME1.3"],""),
("GE1.1","Recognise and name 2D shapes (rectangle, square, circle, triangle) and 3D shapes (cuboid, cube, pyramid, sphere)","Shape sorting, feely bag","Finds the cube from a feely bag by touch",["GE0.1"],""),
("GE1.2","Describe position, direction and movement, including whole, half, quarter and three-quarter turns","Body turns, floor robot","Turns a quarter turn on instruction",["GE0.2"],""),
("AL1.1","Spot and continue number patterns on a hundred square","Coloured hundred square","Continues 5, 10, 15 and says the rule",["NS1.2"],""),
("PS1.1","Draw a picture of a problem and explain thinking using 'because'","Free sketching, bar model","Explains an answer with a drawing",["PS0.1"],""),

# ---------------- STAGE 2 · Year 2 ----------------
("NS2.1","Count in steps of 2, 3 and 5 from 0, and in 10s from any number","Number line, bead string","Counts on in 10s from 23",["NS1.2"],""),
("NS2.2","Know the value of each digit in a two-digit number; partition in different ways (34 = 30 + 4 = 20 + 14)","Base-10 blocks, place-value counters, arrow cards","Shows 43 in two different ways",["NS1.4"],""),
("NS2.3","Compare and order numbers to 100 using <, > and =","Base-10 blocks side by side","Writes 47 < 74 and explains why",["NS2.2"],""),
("NS2.4","Place and estimate numbers on a 0-100 number line","Empty number line","Marks 70 roughly in the right place on a blank 0-100 line",["NS2.2"],"P:R"),
("NS2.5","Read and write numbers to 100 in words","Word cards","Writes 'sixty-eight'",["NS1.3"],""),
("AS2.1","Recall addition and subtraction facts to 20 fluently; derive related facts to 100 (3 + 4 = 7 so 30 + 40 = 70)","Ten-frames, base-10 tens rods","Answers 20 mixed facts in one minute",["AS1.2","AS1.5"],""),
("AS2.2","Add and subtract: 2-digit and 1-digit, 2-digit and tens, two 2-digit numbers, three 1-digit numbers","Base-10 blocks, number line","Solves 46 + 27 and explains the exchange",["AS2.1","NS2.2"],""),
("AS2.3","Know addition is commutative and subtraction is not","Cubes in two colours","Says why 9 - 3 is not the same as 3 - 9",["AS1.4"],""),
("AS2.4","Use inverse relationships and fact families to check calculations","Part-whole triangle","Writes all four facts for 6, 8, 14",["AS2.1"],""),
("AS2.5","Know pairs of multiples of 10 that make 100 (70 + 30)","Ten tens rods, 100 bead string","Answers 100 = 40 + ? instantly",["AS1.1"],""),
("AS2.6","Solve two-step word problems with a bar model (part-whole and comparison)","Bar model","Draws and solves a two-step comparison problem",["AS1.9","AS2.2"],"P:SG"),
("MD2.1","Recall the 2, 5 and 10 times tables; recognise odd and even numbers","Arrays, counting stick","Answers mixed ×2, ×5, ×10 facts in 3 seconds each",["NS2.1"],""),
("MD2.2","Understand multiplication as repeated addition and arrays; know it is commutative","Arrays, number line jumps","Shows 4 × 3 = 3 × 4 with an array",["MD1.1"],""),
("MD2.3","Understand division as sharing and as grouping; write ×, ÷ and = statements","Counters in groups","Shows 12 ÷ 3 both as sharing and grouping",["MD1.1"],""),
("MD2.4","Solve multiplication and division problems in context","Bar model, arrays","Solves 'How many bags of 5 from 30 apples?'",["MD2.3"],""),
("MD2.5","Know all times tables to 9 × 9 (Japanese kuku, Grade 2)","Arrays, chant cards, area grid","Answers 7 × 8 within 3 seconds",["MD2.2"],"P:JP"),
("FR2.1","Find and name 1/3, 1/4, 2/4 and 3/4 of a length, shape or set; know 2/4 = 1/2","Fraction strips, folded paper, counters","Finds 3/4 of 12 counters",["FR1.2"],""),
("ME2.1","Choose units and measure length (cm, m), mass (kg, g), temperature (°C) and capacity (l, ml)","Rulers, scales, jugs, thermometer","Reads a scale to the nearest labelled unit",["ME1.1"],""),
("ME2.2","Compare and order lengths, mass and capacity using <, > and =","Measuring tools","Orders three jugs by capacity",["ME2.1"],""),
("ME2.3","Use £ and p; combine coins to make amounts; find change","Coins, shop role play","Makes 37p in two ways; finds change from 50p",["ME1.2","AS2.2"],""),
("ME2.4","Tell time to 5 minutes, including quarter past and quarter to; know minutes in an hour, hours in a day","Geared clock, counting in 5s","Reads 10:25 on an analogue clock",["ME1.4","NS2.1"],""),
("GE2.1","Describe 2D shapes by sides and vertical line symmetry","Mirrors, folding","Counts sides and finds the mirror line",["GE1.1"],""),
("GE2.2","Describe 3D shapes by edges, vertices and faces","Real solids, straws and putty","Says a cube has 8 vertices",["GE1.1"],""),
("GE2.3","Describe rotations as clockwise and anticlockwise turns; know a quarter turn is a right angle","Floor robot, body turns","Turns a shape a quarter turn clockwise",["GE1.2"],""),
("GE2.4","Compose and split shapes; mentally rotate and fit shapes (tangrams, pentominoes)","Tangrams, pentominoes, digital puzzles","Completes a tangram outline",["GE0.1"],"P:JP"),
("ST2.1","Read and make tally charts, pictograms, block diagrams and tables","Pictograms with picture keys","Answers 'how many more' questions from a pictogram",["NS2.3"],""),
("AL2.1","Solve missing-number sentences with a box as the unknown (? + 7 = 15)","Balance, bar model","Finds the box in 20 - ? = 13",["AS1.7"],""),
("PS2.1","Reason about always / sometimes / never statements","Sorting cards","Decides 'odd + odd is always even' and shows why",["PS1.1"],""),

# ---------------- STAGE 3 · Year 3 ----------------
("NS3.1","Count in 4s, 8s, 50s and 100s; find 10 or 100 more or less","Counting stick, place-value chart","Says 100 more than 947",["NS2.1"],""),
("NS3.2","Know place value in three-digit numbers; compare and order to 1000","Base-10 blocks, place-value counters","Shows 305 with counters and explains the zero",["NS2.2"],""),
("NS3.3","Read and write numbers to 1000 in numerals and words","Place-value chart","Writes 'six hundred and eight'",["NS3.2"],""),
("NS3.4","Show numbers to 1000 on a soroban (Japanese abacus)","Soroban, digital abacus","Sets 472 on a soroban",["NS3.2"],"P:JP"),
("AS3.1","Add and subtract mentally: a three-digit number and ones, tens or hundreds","Place-value chart","Solves 456 + 30 mentally",["NS3.2"],""),
("AS3.2","Use column addition and subtraction up to three digits, with exchanging","Place-value counters beside the written column","Solves 503 - 267 and explains each exchange",["AS2.2","NS3.2"],""),
("AS3.3","Estimate answers and use inverse operations to check","Rounding on a number line","Estimates 298 + 405 as about 700",["AS3.2"],""),
("AS3.4","Solve missing-number and multi-step problems","Bar model","Solves a two-step money problem",["AS2.6"],""),
("MD3.1","Recall the 3, 4 and 8 times tables","Arrays; doubling 2s to 4s to 8s","Answers mixed ×3, ×4, ×8 facts in 3 seconds each",["MD2.1"],""),
("MD3.2","Multiply a two-digit by a one-digit number, mental to formal","Area model, base-10 arrays","Solves 23 × 4 with an area model",["MD3.1","NS3.2"],""),
("MD3.3","Divide a two-digit by a one-digit number mentally and with jottings","Place-value counters shared out","Solves 48 ÷ 4",["MD3.1"],""),
("MD3.4","Solve scaling and correspondence problems (3 hats and 4 coats make 12 outfits)","Tables, tree sketches","Lists all outfits systematically",["MD2.4"],""),
("FR3.1","Count up and down in tenths; know tenths come from dividing by 10","Fraction strips in tenths, number line","Counts 7/10, 8/10, 9/10, 1",["FR2.1"],""),
("FR3.2","Find unit and non-unit fractions of a set of objects","Bar model, counters","Finds 2/5 of 20",["FR2.1","MD3.3"],""),
("FR3.3","Place fractions on a number line and treat them as numbers","Number line, fraction strips","Marks 3/4 between 0 and 1",["FR2.1"],"P:R"),
("FR3.4","Recognise equivalent fractions with small denominators","Fraction wall","Shows 2/6 = 1/3 on a fraction wall",["FR3.3"],""),
("FR3.5","Add and subtract fractions with the same denominator within one whole","Fraction strips","Solves 2/7 + 3/7",["FR3.3"],""),
("FR3.6","Compare and order unit fractions and fractions with the same denominator","Fraction wall","Explains why 1/8 < 1/5",["FR3.4"],""),
("ME3.1","Measure, compare, add and subtract lengths (m, cm, mm), mass and capacity","Rulers, scales, jugs","Adds 1 m 20 cm and 45 cm",["ME2.1"],""),
("ME3.2","Measure the perimeter of simple 2D shapes","String round a shape, squared paper","Finds the perimeter of a rectangle",["ME3.1"],""),
("ME3.3","Add and subtract amounts of money and give change","Coins, shop role play","Finds change from £5 for £3.65",["ME2.3"],""),
("ME3.4","Tell time on analogue clocks with Roman numerals I-XII and on 12- and 24-hour clocks; use seconds, am/pm, days in each month","Clocks, calendar","Reads a time on a Roman-numeral clock",["ME2.4"],""),
("GE3.1","Draw 2D shapes and make 3D shapes","Squared paper, modelling kits","Builds a cuboid from straws",["GE2.2"],""),
("GE3.2","Recognise angles as turns and as properties of shapes; identify right angles and angles greater or smaller","Right-angle checker from folded paper","Sorts angles against a right-angle checker",["GE2.3"],""),
("GE3.3","Identify horizontal, vertical, perpendicular and parallel lines","Geoboards, grid paper","Finds parallel lines in a classroom photo",["GE3.2"],""),
("ST3.1","Interpret and present data in bar charts, pictograms and tables","Bar charts with scales in 2s, 5s, 10s","Answers two-step questions from a bar chart",["ST2.1"],""),
("AL3.1","Describe a pattern or rule in words and use a symbol for an unknown","Growing patterns with cubes","Says how many cubes in the 10th pattern",["AL2.1"],"P:JP"),
("PS3.1","Try several approaches to a non-routine problem and compare them (structured problem solving)","Japanese lesson structure: problem, try, share, compare","Finds two methods and says which is more efficient",["PS2.1"],"P:JP"),

# ---------------- STAGE 4 · Year 4 ----------------
("NS4.1","Count in multiples of 6, 7, 9, 25 and 1000; find 1000 more or less","Counting stick","Counts in 25s to 300",["NS3.1"],""),
("NS4.2","Count backwards through zero to include negative numbers","Vertical number line, thermometer","Says 3 steps below 1 is -2",["NS4.1"],""),
("NS4.3","Know place value in four-digit numbers; order and compare beyond 1000","Place-value counters, chart","Orders 4087, 4870, 4780",["NS3.2"],""),
("NS4.4","Round any number to the nearest 10, 100 or 1000","Number line between two multiples","Rounds 3650 to the nearest 1000",["NS4.3"],""),
("NS4.5","Read Roman numerals to 100 and know how the system changed over time","Clock faces, chapter numbers","Reads XLIV as 44",["ME3.4"],""),
("AS4.1","Use column addition and subtraction with up to four digits","Place-value counters","Solves 4005 - 1738",["AS3.2"],""),
("AS4.2","Solve two-step problems, choosing operations and methods","Bar model","Explains why they chose each operation",["AS3.4"],""),
("MD4.1","Recall all multiplication and division facts to 12 × 12","Arrays, area grid, games with spaced practice","25 mixed facts, 6 seconds each, 23+ correct",["MD3.1","MD2.5"],"T:MTC"),
("MD4.2","Multiply by 0 and 1, divide by 1, multiply three numbers together","Arrays","Solves 2 × 6 × 5 by choosing a good order",["MD4.1"],""),
("MD4.3","Use factor pairs and the distributive law in mental calculation (39 × 7 = 40 × 7 - 7)","Area model","Calculates 19 × 6 mentally",["MD4.1","MD3.2"],""),
("MD4.4","Use short multiplication for two- and three-digit numbers by a one-digit number","Place-value counters beside the column","Solves 346 × 7",["MD4.1","MD3.2"],""),
("MD4.5","Solve integer scaling and harder correspondence problems","Bar model, tables","Solves 'a giraffe is 4 times as tall as a 1.3 m child'",["MD3.4"],""),
("FR4.1","Recognise hundredths from dividing by 100 and dividing tenths by 10","100 square, place-value chart","Shades 0.07 of a hundred square",["FR3.1"],""),
("FR4.2","Recognise families of equivalent fractions","Fraction wall, multiplication grid","Lists four fractions equal to 2/3",["FR3.4","MD4.1"],""),
("FR4.3","Find non-unit fractions of quantities (3/5 of 40)","Bar model","Solves 3/8 of 64",["FR3.2"],""),
("FR4.4","Add and subtract fractions with the same denominator, including beyond 1","Fraction strips, number line","Solves 5/6 + 4/6",["FR3.5"],""),
("FR4.5","Know decimal equivalents of tenths, hundredths, 1/4, 1/2 and 3/4","Hundred square, number line","Writes 3/4 as 0.75",["FR4.1"],""),
("FR4.6","Divide one- and two-digit numbers by 10 and 100","Place-value slider (digits move, point stays)","Writes 37 ÷ 100 = 0.37",["FR4.1"],""),
("FR4.7","Round 1-place decimals to the nearest whole; compare decimals to 2 places","Number line","Orders 0.5, 0.45, 0.54",["FR4.5"],""),
("FR4.8","Solve simple money problems with decimals to 2 places","Coins, price tags","Totals £2.45 + £1.80",["FR4.7","ME3.3"],""),
("ME4.1","Convert between units (km/m, m/cm, cm/mm, hours/minutes)","Conversion number lines","Writes 3.5 km as 3500 m",["ME3.1","FR4.6"],""),
("ME4.2","Find perimeter of rectilinear shapes and area by counting squares","Squared paper, geoboard","Finds area of an L-shape by counting",["ME3.2"],""),
("ME4.3","Convert between analogue and digital 12- and 24-hour times","Dual clock","Writes 3:40 pm as 15:40",["ME3.4"],""),
("GE4.1","Compare and classify triangles and quadrilaterals by their properties","Venn/Carroll sorting, geoboards","Sorts quadrilaterals by parallel sides",["GE3.3"],""),
("GE4.2","Identify acute and obtuse angles; order angles up to two right angles","Angle fans, right-angle checker","Orders four angles by size",["GE3.2"],""),
("GE4.3","Identify lines of symmetry in different orientations; complete a symmetric figure","Mirrors, grid paper","Completes a figure across a diagonal line",["GE2.1"],""),
("GE4.4","Use coordinates in the first quadrant; plot points to draw a polygon","Grid games (battleships)","Plots the fourth corner of a square",["GE3.3"],""),
("GE4.5","Describe translations left, right, up and down","Grid, sliding cut-out shapes","Describes a move as 3 right, 2 up",["GE4.4"],""),
("ST4.1","Use bar charts and time graphs for discrete and continuous data; solve sum and difference problems","Line graph of temperature","Reads a value between gridlines",["ST3.1"],""),
("AL4.1","Write a rule in words and then with a letter (perimeter of a square = 4 × s)","Growing patterns, function machines","Writes a rule for a pattern of matchsticks",["AL3.1"],"P:SG"),

# ---------------- STAGE 5 · Year 5 ----------------
("NS5.1","Read, write, order and compare numbers to 1,000,000","Place-value chart to millions","Orders five six-digit numbers",["NS4.3"],""),
("NS5.2","Count forwards and backwards in powers of 10","Place-value chart","Counts back in 10,000s from 92,000",["NS5.1"],""),
("NS5.3","Use negative numbers in context; find intervals across zero","Thermometer, vertical number line","Finds the difference between -4 °C and 7 °C",["NS4.2"],""),
("NS5.4","Round any number to 1,000,000 to the nearest 10, 100, 1000, 10,000 or 100,000","Number line","Rounds 456,789 to the nearest 10,000",["NS4.4"],""),
("NS5.5","Read Roman numerals to 1000 (M) and years in Roman numerals","Building inscriptions","Reads MMXXVI",["NS4.5"],""),
("AS5.1","Add and subtract numbers with more than four digits, written and mental","Column method, number line","Solves 120,450 - 87,996",["AS4.1"],""),
("AS5.2","Solve multi-step problems; use rounding to check","Bar model","Explains if an answer is reasonable",["AS4.2"],""),
("MD5.1","Identify multiples, factors and common factors","Arrays, factor rainbows","Lists all factors of 36",["MD4.1"],""),
("MD5.2","Know primes to 19 by heart and find primes to 100; split numbers into prime factors","Sieve of Eratosthenes, factor trees","Writes 60 as 2 × 2 × 3 × 5",["MD5.1"],""),
("MD5.3","Recognise square and cube numbers and their notation (² and ³)","Real squares and cubes of cubes","Says 4³ = 64 and shows it with cubes",["MD4.1"],""),
("MD5.4","Multiply up to four digits by one or two digits, including long multiplication","Area model beside long multiplication","Solves 1,342 × 26",["MD4.4"],""),
("MD5.5","Divide up to four digits by one digit using short division; interpret remainders","Place-value counters, bus-stop method","Solves 4,327 ÷ 6 and says what the remainder means",["MD4.1"],""),
("MD5.6","Multiply and divide whole numbers and decimals by 10, 100 and 1000","Place-value slider","Writes 4.7 × 100 = 470",["FR4.6"],""),
("MD5.7","Solve problems involving scaling by simple fractions and simple rates","Bar model","Solves 'half as long again'",["MD4.5"],""),
("FR5.1","Compare and order fractions whose denominators are multiples of the same number","Fraction wall","Orders 2/3, 5/6, 7/12",["FR4.2"],""),
("FR5.2","Identify equivalent fractions, including tenths and hundredths","Hundred square","Writes 3/10 = 30/100",["FR4.2"],""),
("FR5.3","Convert between mixed numbers and improper fractions","Fraction strips beyond 1","Writes 17/5 as 3 2/5",["FR4.4"],""),
("FR5.4","Add and subtract fractions with the same or related denominators","Fraction strips","Solves 3/4 + 5/8",["FR5.1"],""),
("FR5.5","Multiply proper fractions and mixed numbers by whole numbers","Bar model, repeated addition","Solves 2 3/4 × 3",["FR5.3"],""),
("FR5.6","Read and write decimals as fractions (0.71 = 71/100); know thousandths","Place-value chart to thousandths","Writes 0.035 as a fraction",["FR4.5"],""),
("FR5.7","Round decimals with 2 places; order decimals to 3 places","Number line zoom","Orders 0.3, 0.301, 0.31",["FR4.7"],""),
("FR5.8","Understand percent as 'per hundred'; convert between key fractions, decimals and percentages","Hundred square, double number line","Says 2/5 = 0.4 = 40%",["FR5.2"],""),
("ME5.1","Convert between metric units; know approximate imperial equivalents (inches, pounds, pints)","Conversion lines","Says 1 inch is about 2.5 cm",["ME4.1"],""),
("ME5.2","Find perimeter of composite shapes and area of rectangles (cm², m²); estimate irregular areas","Squared paper","Finds the area of a 12 cm by 7 cm rectangle",["ME4.2","MD4.1"],""),
("ME5.3","Estimate volume and capacity; use cm³","Cube models","Builds a 3 × 2 × 2 shape and says its volume",["MD5.3"],""),
("ME5.4","Solve problems with time and read timetables","Bus and train timetables","Plans a journey from a timetable",["ME4.3"],""),
("GE5.1","Identify 3D shapes from 2D drawings and nets","Isometric drawings, nets to fold","Matches a net to its cube",["GE3.1"],""),
("GE5.2","Measure and draw angles in degrees with a protractor; name acute, obtuse and reflex","Protractor, digital angle tool","Draws a 135° angle",["GE4.2"],""),
("GE5.3","Know angles at a point total 360°, on a straight line 180°; find missing angles","Paper-tearing angle demos","Finds a missing angle on a line",["GE5.2"],""),
("GE5.4","Use properties of rectangles; tell regular from irregular polygons","Geoboard","Explains why a rhombus is not regular",["GE4.1"],""),
("GE5.5","Reflect and translate shapes on a grid","Coordinate grid","Reflects a triangle in a line",["GE4.5"],""),
("ST5.1","Solve problems with line graphs; read and complete two-way tables","Line graphs, timetables","Reads change between two points on a line graph",["ST4.1"],""),
("AL5.1","Continue and describe number sequences with a constant step, including decimals and negatives","Number line","Continues 2.4, 2.1, 1.8",["AL4.1"],""),

# ---------------- STAGE 6 · Year 6 ----------------
("NS6.1","Read, write, order and compare numbers to 10,000,000; round to any degree of accuracy","Place-value chart","Rounds 7,456,320 to the nearest 100,000",["NS5.1"],"T:SATs"),
("NS6.2","Use negative numbers in context and calculate intervals across zero","Number line","Solves -6 + 9",["NS5.3"],"T:SATs"),
("MD6.1","Divide up to four digits by two digits using long division; show remainders as whole numbers, fractions or decimals","Long division with a multiples list","Solves 4,784 ÷ 23",["MD5.5","MD5.4"],"T:SATs"),
("MD6.2","Multiply up to four digits by two digits using long multiplication","Area model","Solves 3,429 × 47 accurately",["MD5.4"],"T:SATs"),
("MD6.3","Use the order of operations, including brackets","Expression trees","Solves 4 + 6 × (8 - 3)",["MD5.4"],"T:SATs"),
("MD6.4","Find common factors, common multiples and primes","Venn diagram of factors","Finds the lowest common multiple of 6 and 8",["MD5.2"],"T:SATs"),
("MD6.5","Calculate mentally with mixed operations and large numbers; estimate to check","Number line, rounding","Completes a 30-minute arithmetic paper",["MD6.3"],"T:SATs"),
("FR6.1","Simplify fractions using common factors; use common denominators","Fraction wall","Simplifies 18/24",["FR5.1","MD6.4"],"T:SATs"),
("FR6.2","Compare and order fractions, including fractions greater than 1","Number line","Orders 5/3, 1 1/2, 7/4",["FR6.1"],"T:SATs"),
("FR6.3","Add and subtract fractions with different denominators and mixed numbers","Fraction strips, common-denominator grids","Solves 2 1/3 - 3/4",["FR6.1"],"T:SATs"),
("FR6.4","Multiply simple pairs of proper fractions (1/4 × 1/2 = 1/8)","Area model on a square","Shows 2/3 × 3/4 with an area diagram",["FR5.5"],"T:SATs"),
("FR6.5","Divide proper fractions by whole numbers (1/3 ÷ 2 = 1/6)","Bar model","Solves 3/5 ÷ 2",["FR6.4"],"T:SATs"),
("FR6.6","Convert fractions to decimals by division (3/8 = 0.375)","Short division","Writes 5/8 as a decimal",["MD5.5","FR5.6"],"T:SATs"),
("FR6.7","Multiply one-digit decimals by whole numbers; divide giving answers to 2 decimal places","Place-value counters","Solves 0.7 × 8 and 9 ÷ 4",["MD5.6"],"T:SATs"),
("FR6.8","Find percentages of amounts and use them to compare","Bar model, double number line","Finds 35% of 60",["FR5.8"],"T:SATs"),
("RP6.1","Compare relative sizes using multiplication and division ('for every 2 red, 3 blue')","Bar model, ratio tables","Solves 'for every 2 boys there are 3 girls; 15 girls, how many boys?'",["MD5.7"],"T:SATs"),
("RP6.2","Find missing values using integer multiplication facts; use scale factors and similar shapes","Double number line, enlargement on grids","Finds the missing side of an enlarged shape",["RP6.1"],"T:SATs"),
("RP6.3","Solve unequal sharing and grouping problems using fractions and multiples","Bar model","Shares £45 in the ratio 2:7",["RP6.1"],"T:SATs"),
("AL6.1","Use simple formulae","Function machines","Uses cost = 3n + 2 for n = 5",["AL4.1"],"T:SATs"),
("AL6.2","Generate and describe linear number sequences","Pattern tables","Finds the 10th term of 3, 7, 11",["AL5.1"],"T:SATs"),
("AL6.3","Write missing-number problems algebraically","Bar model, balance","Writes and solves 2a + 5 = 17",["AL2.1","AL6.1"],"T:SATs"),
("AL6.4","Find pairs of numbers that satisfy an equation with two unknowns; list possibilities systematically","Tables","Lists all whole-number pairs with a + b = 7 and a > b",["AL6.3"],"T:SATs"),
("ME6.1","Convert units of measure using decimals to 3 places; convert miles and km","Conversion graph","Writes 5 miles as about 8 km",["ME5.1"],"T:SATs"),
("ME6.2","Know shapes with the same area can have different perimeters, and vice versa","Squared paper, pentominoes","Draws two shapes with area 12 and different perimeters",["ME5.2"],"T:SATs"),
("ME6.3","Calculate the area of parallelograms and triangles using formulae","Cut-and-move rearrangement","Finds the area of a triangle with base 8 and height 5",["ME5.2"],"T:SATs"),
("ME6.4","Calculate volume of cubes and cuboids (cm³, m³) using a formula","Cube building","Finds volume of a 4 × 3 × 5 cuboid",["ME5.3"],"T:SATs"),
("GE6.1","Draw 2D shapes from given lengths and angles; recognise and build nets","Protractor, net folding","Draws a triangle with sides 6 cm and 4 cm and angle 50°",["GE5.1","GE5.2"],"T:SATs"),
("GE6.2","Find missing angles in triangles, quadrilaterals and regular polygons; know vertically opposite angles","Paper-tearing demos","Finds the interior angle of a regular hexagon",["GE5.3"],"T:SATs"),
("GE6.3","Name parts of a circle (radius, diameter, circumference); know diameter is twice the radius","Compasses, string","Says diameter 14 cm means radius 7 cm",["GE5.4"],"T:SATs"),
("GE6.4","Use coordinates in all four quadrants; translate and reflect shapes","Four-quadrant grid","Reflects a shape in the y-axis",["GE5.5","NS6.2"],"T:SATs"),
("ST6.1","Interpret and construct pie charts and line graphs","Pie chart as a 'fraction circle'","Reads 1/4 of a pie of 40 as 10",["ST5.1","FR6.8"],"T:SATs"),
("ST6.2","Calculate and interpret the mean","Levelling towers of cubes","Finds the mean of 4, 7, 9, 12",["MD5.5"],"T:SATs"),
("PS6.1","Solve multi-step reasoning problems and justify answers in writing","Bar model, worked examples","Explains each step of a two-mark reasoning question",["PS3.1"],"T:SATs"),

# ---------------- STAGE 7 · Year 7 ----------------
("NS7.1","Order integers, decimals and fractions, including negatives, on one number line","Number line","",["NS6.2","FR6.2"],""),
("NS7.2","Use the four operations with negative numbers","Two-colour counters, number line","",["NS6.2"],""),
("NS7.3","Use powers and roots: squares, cubes, square roots, cube roots, index notation","Area and volume models","",["MD5.3"],""),
("NS7.4","Use prime factorisation to find HCF and LCM","Venn diagram of prime factors","",["MD6.4"],""),
("NS7.5","Round to decimal places and significant figures; estimate answers","Number line","",["NS6.1"],""),
("FR7.1","Use the four operations with fractions and mixed numbers","Area model, bar model","",["FR6.3","FR6.5"],""),
("FR7.2","Convert between fractions, decimals and percentages, including simple recurring decimals","Double number line","",["FR6.6"],""),
("FR7.3","Calculate percentage increase and decrease using multipliers","Bar model","",["FR6.8"],""),
("AL7.1","Use algebraic notation (3y, ab, a², a/b) and collect like terms","Algebra tiles","",["AL6.3"],""),
("AL7.2","Substitute numbers into expressions and formulae","Function machines","",["AL6.1"],""),
("AL7.3","Expand single brackets and factorise simple expressions","Algebra tiles, area model","",["AL7.1"],""),
("AL7.4","Solve linear equations in one or two steps","Balance model, bar model","",["AL6.3"],""),
("AL7.5","Find term-to-term and position-to-term (nth term) rules for linear sequences","Pattern tables","",["AL6.2"],""),
("RP7.1","Use ratio notation, simplify ratios, share in a ratio","Bar model, ratio tables","",["RP6.3"],""),
("RP7.2","Solve direct proportion problems with the unitary method","Double number line","",["RP6.2"],""),
("GE7.1","Use angle facts with parallel lines (alternate, corresponding), triangles and polygons","Dynamic geometry","",["GE6.2"],""),
("GE7.2","Construct bisectors and triangles with ruler and compasses","Compasses","",["GE6.1"],""),
("GE7.3","Find perimeter and area of triangles, parallelograms, trapezia and compound shapes","Cut-and-rearrange","",["ME6.3"],""),
("ST7.1","Find mean, median, mode and range; choose a suitable average","Ordered data lines","",["ST6.2"],""),
("ST7.2","Draw and interpret bar charts, pie charts, frequency tables and stem-and-leaf diagrams","Chart builder","",["ST6.1"],""),
("PB7.1","Use the 0-1 probability scale; know P(not A) = 1 - P(A)","Probability line, spinners","",["FR6.6"],""),

# ---------------- STAGE 8 · Year 8 ----------------
("NS8.1","Write and calculate with numbers in standard form","Place-value chart","",["NS7.3"],""),
("NS8.2","Use the laws of indices for integer powers","Expanded products","",["NS7.3"],""),
("FR8.1","Solve reverse percentage, repeated percentage change and simple/compound interest problems","Bar model, multiplier chains","",["FR7.3"],""),
("AL8.1","Expand products of two brackets","Area model, algebra tiles","",["AL7.3"],""),
("AL8.2","Solve equations with unknowns on both sides and with brackets; form equations from context","Balance model","",["AL7.4"],""),
("AL8.3","Solve linear inequalities and show them on a number line","Number line","",["AL8.2"],""),
("AL8.4","Plot linear graphs; interpret gradient and intercept (y = mx + c)","Dynamic graphing","",["AL7.2","GE6.4"],""),
("AL8.5","Interpret real-life graphs (distance-time, conversion)","Graph stories","",["AL8.4"],""),
("AL8.6","Rearrange simple formulae","Balance model, function machines","",["AL8.2"],""),
("RP8.1","Use compound measures: speed, density, pressure","Formula triangles, unit tables","",["RP7.2"],""),
("RP8.2","Recognise inverse proportion; compare best buys","Tables, graphs","",["RP7.2"],""),
("GE8.1","Calculate circumference and area of circles using π","Unrolled circle, sector rearrangement","",["GE6.3"],""),
("GE8.2","Find volume and surface area of prisms and cylinders","Nets, layers of cubes","",["ME6.4"],""),
("GE8.3","Rotate, reflect, translate and enlarge shapes (positive scale factors)","Dynamic geometry","",["GE6.4"],""),
("GE8.4","Use bearings and scale drawings","Maps, protractor","",["GE5.2","RP7.2"],""),
("ST8.1","Draw and interpret scatter graphs and correlation","Scatter plots of real data","",["ST7.2"],""),
("ST8.2","Estimate averages from grouped frequency tables","Grouped tables","",["ST7.1"],""),
("PB8.1","List sample spaces for two events; compare experimental and theoretical probability","Two-way tables, simulations","",["PB7.1"],""),
("PB8.2","Use Venn diagrams and set notation","Venn diagrams","",["PB8.1"],""),

# ---------------- STAGE 9 · Year 9 ----------------
("NS9.1","Use error intervals and upper and lower bounds","Number line intervals","",["NS7.5"],""),
("AL9.1","Factorise quadratics x² + bx + c and solve by factorising","Algebra tiles","",["AL8.1"],""),
("AL9.2","Solve simultaneous linear equations algebraically and graphically","Graphs crossing","",["AL8.2","AL8.4"],""),
("AL9.3","Plot quadratic graphs; find roots and turning points","Dynamic graphing","",["AL9.1"],""),
("AL9.4","Recognise quadratic, geometric and Fibonacci-type sequences","Difference tables","",["AL7.5"],""),
("AL9.5","Write simple algebraic arguments and proofs ('show that')","Worked examples","",["AL8.1"],""),
("GE9.1","Use Pythagoras' theorem in 2D","Squares on the sides, dissection proof","",["NS7.3"],""),
("GE9.2","Use right-angled trigonometry (sin, cos, tan)","Unit circle, similar triangles","",["GE9.1","RP6.2"],""),
("GE9.3","Use congruence criteria and similarity","Dynamic geometry","",["GE8.3"],""),
("GE9.4","Use column vectors: add, subtract and scale","Arrows on a grid","",["GE8.3"],""),
("GE9.5","Construct loci","Compasses","",["GE7.2"],""),
("RP9.1","Write direct and inverse proportion algebraically (y ∝ x, y ∝ 1/x)","Graphs","",["RP8.2"],""),
("RP9.2","Model growth and decay","Multiplier chains, graphs","",["FR8.1"],""),
("PB9.1","Use tree diagrams for independent and dependent events","Tree diagrams","",["PB8.1"],""),

# ---------------- STAGE 10 · GCSE Foundation ----------------
("NS10.1","Calculate fluently without a calculator, giving exact answers with fractions and π","","",["FR7.1"],"T:GCSE"),
("NS10.2","Use the product rule for counting combinations","Tables, tree sketches","",["MD3.4"],"T:GCSE"),
("FR10.1","Solve financial percentage problems: compound interest, depreciation, VAT","","",["FR8.1"],"T:GCSE"),
("RP10.1","Combine ratios and link ratios to fractions and linear functions","Bar model","",["RP7.1"],"T:GCSE"),
("AL10.1","Solve quadratic equations by factorising and find approximate roots from graphs","","",["AL9.1","AL9.3"],"T:GCSE"),
("AL10.2","Recognise and sketch linear, quadratic, cubic and reciprocal graphs","Dynamic graphing","",["AL9.3"],"T:GCSE"),
("AL10.3","Find the equation of a line through two points; parallel lines","","",["AL8.4"],"T:GCSE"),
("GE10.1","Know exact trig values for 0°, 30°, 45°, 60° and 90°","Special triangles","",["GE9.2"],"T:GCSE"),
("GE10.2","Find volume and surface area of spheres, cones and pyramids; arc length and sector area","","",["GE8.1","GE8.2"],"T:GCSE"),
("GE10.3","Use similarity and enlargement, including fractional scale factors","","",["GE9.3"],"T:GCSE"),
("ST10.1","Understand sampling and bias; compare distributions using averages and spread","","",["ST7.1"],"T:GCSE"),
("PB10.1","Use frequency trees, Venn diagrams and tree diagrams to find probabilities","","",["PB9.1","PB8.2"],"T:GCSE"),
("PS10.1","Solve multi-step problems that combine topics and explain reasoning","Worked examples, mixed practice","",["PS6.1"],"T:GCSE"),

# ---------------- STAGE 11 · GCSE Higher only ----------------
("NS11.1","Simplify surds and rationalise denominators","","",["NS7.3"],"T:GCSE"),
("NS11.2","Use fractional and negative indices","","",["NS8.2"],"T:GCSE"),
("NS11.3","Convert recurring decimals to fractions and prove it","","",["FR7.2"],"T:GCSE"),
("AL11.1","Solve quadratics using the formula and by completing the square","Algebra tiles (completing the square)","",["AL10.1"],"T:GCSE"),
("AL11.2","Simplify and solve equations with algebraic fractions","","",["FR7.1","AL9.1"],"T:GCSE"),
("AL11.3","Use function notation, composite and inverse functions","Function machines","",["AL7.2"],"T:GCSE"),
("AL11.4","Find approximate solutions by iteration","Spreadsheet","",["AL10.1"],"T:GCSE"),
("AL11.5","Transform graphs (y = f(x + a), y = f(x) + a, reflections)","Dynamic graphing","",["AL10.2"],"T:GCSE"),
("AL11.6","Estimate gradients and areas under graphs and interpret them as rates","","",["AL8.5"],"T:GCSE"),
("AL11.7","Solve quadratic inequalities and non-linear simultaneous equations","","",["AL11.1","AL9.2"],"T:GCSE"),
("AL11.8","Use the equation of a circle centred at the origin and find tangents","","",["GE9.1","AL10.3"],"T:GCSE"),
("GE11.1","Use the sine rule, cosine rule and ½ab sin C","","",["GE9.2"],"T:GCSE"),
("GE11.2","Apply Pythagoras and trigonometry in 3D","","",["GE11.1"],"T:GCSE"),
("GE11.3","Prove and apply circle theorems","Dynamic geometry","",["GE7.1"],"T:GCSE"),
("GE11.4","Use vectors in geometric proofs","","",["GE9.4"],"T:GCSE"),
("GE11.5","Sketch trigonometric and exponential graphs","Unit circle animation","",["GE10.1"],"T:GCSE"),
("ST11.1","Draw and interpret histograms, cumulative frequency and box plots","","",["ST10.1"],"T:GCSE"),
("PB11.1","Calculate conditional probabilities","Two-way tables, trees","",["PB10.1"],"T:GCSE"),
("PS11.1","Construct rigorous algebraic proofs","","",["AL9.5"],"T:GCSE"),
]

SOURCES = {"JP": "Japan", "SG": "Singapore", "FI": "Finland", "R": "Research evidence"}

def parse(row):
    oid, text, vis, check, pre, tag = row
    m = re.match(r"([A-Z]+)(\d+)\.(\d+)$", oid)
    strand, stage = m.group(1), int(m.group(2))
    kind, src = "core", None
    if tag.startswith("T:"):
        kind, src = "tested", TESTS[tag[2:]]
    elif tag.startswith("P:"):
        kind, src = "beyond", SOURCES[tag[2:]]
    label, uk, age = STAGES[stage]
    return {
        "id": oid, "stage": stage, "stageName": label, "ukYear": uk, "age": age,
        "strand": strand, "strandName": STRANDS[strand], "objective": text,
        "visualModel": vis, "masteryCheck": check, "prerequisites": pre,
        "kind": kind, "source": src,
        "scenes": ANIM[oid][0].split("+"),
        "animation": ANIM[oid][1],
        "interaction": ANIM[oid][2],
    }

def main():
    out = pathlib.Path(__file__).parent
    missing = [r[0] for r in R if r[0] not in ANIM]
    assert not missing, f"objectives without an animation storyboard: {missing}"
    extra = set(ANIM) - {r[0] for r in R}
    assert not extra, f"storyboards for unknown objectives: {extra}"
    objs = [parse(r) for r in R]
    for o in objs:
        for sc in o["scenes"]:
            assert sc in SCENES, f"{o['id']} uses unknown scene {sc}"
    ids = {o["id"] for o in objs}
    assert len(ids) == len(objs), "duplicate id"
    for o in objs:
        for p in o["prerequisites"]:
            assert p in ids, f"{o['id']} -> missing prerequisite {p}"
    data = {
        "stages": [{"stage": k, "name": v[0], "ukYear": v[1], "age": v[2]} for k, v in STAGES.items()],
        "strands": [{"code": k, "name": v} for k, v in STRANDS.items()],
        "scenes": [{"id": k, "name": v[0], "description": v[1], "motions": v[2],
                    "usedBy": [o["id"] for o in objs if k in o["scenes"]]} for k, v in SCENES.items()],
        "objectives": objs,
    }
    (out / "objectives.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    with open(out / "objectives.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "stage", "ukYear", "age", "strand", "objective", "visualModel", "masteryCheck", "prerequisites", "kind", "source", "scenes", "animation", "interaction"])
        for o in objs:
            w.writerow([o["id"], o["stage"], o["ukYear"], o["age"], o["strandName"], o["objective"], o["visualModel"],
                        o["masteryCheck"], " ".join(o["prerequisites"]), o["kind"], o["source"] or "",
                        " ".join(o["scenes"]), o["animation"], o["interaction"]])
    print(len(objs), "objectives")
    from collections import Counter
    print(Counter(o["stage"] for o in objs))
    print(Counter(o["kind"] for o in objs))

if __name__ == "__main__":
    main()
