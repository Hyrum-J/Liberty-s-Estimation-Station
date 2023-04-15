from tkinter import *
from tkinter import ttk
from tkcalendar import *
import customtkinter
from openpyxl import load_workbook
import AIPredictor as LESter

LESter.train()

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()
root.title("Liberty's Estimation Station")
root.iconbitmap('D:\Coding\Python\Liberty\LES.ico')
root.option_add( "*font", "BondiMT 12" )


isBasementFinished = 0
secondTrue = 0

def datePicker(event):
    global estimatedDateCalendar, calendar
    
    calendar = customtkinter.CTkToplevel()
    calendar.grab_set()
    calendar.resizable(False, False)
    calendar.title('Estimated Completion Date')
    calendar.geometry('250x220+590+370')
    estimatedDateCalendar = Calendar(calendar, selectmode = "day", year = 2023, month = 3, date_pattern='MM/dd/yyyy')
    estimatedDateCalendar.place(x = 0, y = 0)

    submitButton = customtkinter.CTkButton(calendar, text = "Submit", command = grabDate)
    submitButton.place(x = 60, y = 190)

def grabDate():
    global calculateButton
    selectedDate.delete(0, END)
    selectedDate.insert(0, estimatedDateCalendar.get_date())
    calculateButton.configure(state = NORMAL)
    calendar.destroy()
    
def update():
    global secondExist
    global isBasementFinished
    global secondTrue
    global mainSqft
    global secondSqft
    global garageSqft
    global basementSqft

    isBasementFinished = finishedVar.get()
    secondTrue = secondVar.get()
    secondExist = secondSqftLabel.winfo_exists()
    secondString = StringVar()
    mainString = mainSqftEntry.get()
    basementString = basementSqftEntry.get()
    garageString = garageSqftEntry.get()
    
    if mainString.isnumeric():
        mainSqft = int(mainSqftEntry.get())
    else:
        mainSqft = 0

    if secondExist == 1:
        secondString = secondSqftEntry.get()
        if secondString.isnumeric():
            secondSqft = int(secondSqftEntry.get())
        else:
            secondSqft = 0
    
    if basementString.isnumeric():
        basementSqft = int(basementSqftEntry.get())
    else:
        basementSqft = 0
    
    if garageString.isnumeric():
        garageSqft = int(garageSqftEntry.get())
    else:
        garageSqft = 0

    if secondExist == 1:
        totalSqftOutput.configure(text = str(mainSqft+secondSqft+basementSqft+garageSqft))
    else:
        totalSqftOutput.configure(text = str(mainSqft+basementSqft+garageSqft))
    totalSqftOutput.after(1000, update)

def updateCheck():
    if secondVar.get() == 1:
        secondSqftLabel.grid(row = 4, column = 0)
        secondSqftEntry.grid(row = 5, column = 0)
    elif secondExist == 1:
        secondSqftLabel.grid_forget()
        secondSqftEntry.delete(0, END)
        secondSqftEntry.insert(0, "0")
        secondSqftEntry.grid_forget()

def calculationClick():
    global secondTrue
    global isBasementFinished

    stringDate = str(selectedDate.get())

    if locationDropdown.get() == "Idaho Falls":
        location = 0
    elif locationDropdown.get() == "Ammon":
        location = 1
    elif locationDropdown.get() == "Iona":
        location = 2
    elif locationDropdown.get() == "Bonneville County":
        location = 3

    doesExist = secondTrue
    isFinished = isBasementFinished
    
    if(doesExist == 1):
        garageFinalSqft = garageSqft
        mainFinalSqft = mainSqft
        basementFinalSqft = basementSqft
        secondFinalSqft = secondSqft
        finalSqft = garageFinalSqft + mainFinalSqft + basementFinalSqft + secondFinalSqft
    else:
        garageFinalSqft = garageSqft
        mainFinalSqft = mainSqft
        basementFinalSqft = basementSqft
        finalSqft = garageFinalSqft + mainFinalSqft + basementFinalSqft

    LESter.predict(int(stringDate[0:2]), int(stringDate[3:5]), int(stringDate[6:10]), location, finalSqft)

    path = "LibertyPriceBook.xlsx"
    
    workbook = load_workbook(path)
    spreadsheet = workbook.active

    permitCost = round(spreadsheet["B2"].value * finalSqft, 2)
    engineeringCost = round(spreadsheet["B3"].value * finalSqft, 2)
    trussCostTotal = round(spreadsheet["B4"].value * finalSqft, 2)
    roofingCostSqft = round(spreadsheet["B5"].value * finalSqft, 2)
    roofingLaborCost = round(spreadsheet["B6"].value * finalSqft, 2)
    roofingCostTotal = roofingCostSqft + roofingLaborCost
    brickCostSqft = round(spreadsheet["B7"].value * finalSqft, 2)
    brickCostLabor = round(spreadsheet["B8"].value * finalSqft, 2)
    brickCostTotal = brickCostSqft + brickCostLabor
    sidingCostSqft = round(spreadsheet["B25"].value * finalSqft, 2)
    sidingCostLabor = round(spreadsheet["B26"].value * finalSqft, 2)
    sidingCostTotal = sidingCostSqft + sidingCostLabor

    totalOtherCost = permitCost + engineeringCost + trussCostTotal + roofingCostTotal + brickCostTotal + sidingCostTotal

    
    lumberSqft = round(spreadsheet["B9"].value, 2)
    framingMainCostSqft = round(spreadsheet["B10"].value * mainFinalSqft, 2)
    electricalMainCostSqft = round(spreadsheet["B11"].value * mainFinalSqft, 2)
    plumbingMainCostSqft = round(spreadsheet["B12"].value * mainFinalSqft, 2)
    sheetrockMainCostSqft = round(spreadsheet["B13"].value * mainFinalSqft, 2)
    sheetrockMainCostLabor = round(spreadsheet["B14"].value * mainFinalSqft, 2)
    sheetrockMainCostTotal = sheetrockMainCostSqft + sheetrockMainCostLabor    
    paintingMainCostSqft = round(spreadsheet["B15"].value * mainFinalSqft, 2)
    heatingMainCostSqft = round(spreadsheet["B16"].value * mainFinalSqft, 2)
    insulationMainCostSqft = round(spreadsheet["B17"].value * mainFinalSqft, 2)
    trimMainCostSqft = round(spreadsheet["B18"].value * mainFinalSqft, 2)
    trimMainCostLabor = round(spreadsheet["B19"].value * mainFinalSqft, 2)
    trimMainCostTotal = trimMainCostSqft + trimMainCostLabor

    mainCostTotal = (lumberSqft * mainFinalSqft) + framingMainCostSqft + electricalMainCostSqft + plumbingMainCostSqft + sheetrockMainCostTotal + paintingMainCostSqft + heatingMainCostSqft + insulationMainCostSqft + trimMainCostTotal

    if(doesExist == 1):
        framingSecondCostSqft = round(spreadsheet["B10"].value * secondFinalSqft, 2)
        electricalSecondCostSqft = round(spreadsheet["B11"].value * secondFinalSqft, 2)
        plumbingSecondCostSqft = round(spreadsheet["B12"].value * secondFinalSqft, 2)
        sheetrockSecondCostSqft = round(spreadsheet["B13"].value * secondFinalSqft, 2)
        sheetrockSecondCostLabor = round(spreadsheet["B14"].value * secondFinalSqft, 2)
        sheetrockSecondCostTotal = sheetrockSecondCostSqft + sheetrockSecondCostLabor
        paintingSecondCostSqft = round(spreadsheet["B15"].value * secondFinalSqft, 2)
        heatingSecondCostSqft = round(spreadsheet["B16"].value * secondFinalSqft, 2)
        insulationSecondCostSqft = round(spreadsheet["B17"].value * secondFinalSqft, 2)
        trimSecondCostSqft = round(spreadsheet["B18"].value * secondFinalSqft, 2)
        trimSecondCostLabor = round(spreadsheet["B19"].value * secondFinalSqft, 2)
        trimSecondCostTotal = trimSecondCostSqft + trimSecondCostLabor

        secondCostTotal = (lumberSqft * secondFinalSqft) + framingSecondCostSqft + electricalSecondCostSqft + plumbingSecondCostSqft + sheetrockSecondCostTotal + paintingSecondCostSqft + heatingSecondCostSqft + insulationSecondCostSqft + trimSecondCostTotal

    
    framingBasementCostSqft = round(spreadsheet["B10"].value * basementFinalSqft, 2)
    insulationBasementCostSqft = round(spreadsheet["B17"].value * basementFinalSqft, 2)
    heatingBasementCostSqft = round(spreadsheet["B16"].value * basementFinalSqft, 2)
    concreteBasementCostSqft = round(spreadsheet["B20"].value * basementFinalSqft, 2)
    concreteBasementCostLabor = round(spreadsheet["B21"].value * basementFinalSqft, 2)
    concreteBasementCostTotal = concreteBasementCostSqft + concreteBasementCostLabor
    foundatoinCost = round(spreadsheet["B22"].value * finalSqft, 2)
    excavationBasementCost = round(spreadsheet["B23"].value * basementFinalSqft, 2)
    gravelBasementCost = round(spreadsheet["B24"].value * basementFinalSqft, 2)

    if(isFinished == 1):
        electricalBasementCostSqft = round(spreadsheet["B11"].value * basementFinalSqft, 2)
        plumbingBasementCostSqft = round(spreadsheet["B12"].value * basementFinalSqft, 2)
        sheetrockBasementCostSqft = round(spreadsheet["B13"].value * basementFinalSqft, 2)
        sheetrockBasementCostLabor = round(spreadsheet["B14"].value * basementFinalSqft, 2)
        sheetrockBasementCostTotal = sheetrockBasementCostSqft + sheetrockBasementCostLabor
        paintingBasementCostSqft = round(spreadsheet["B15"].value * basementFinalSqft, 2)
        trimBasementCostSqft = round(spreadsheet["B18"].value * basementFinalSqft, 2)
        trimBasementCostLabor = round(spreadsheet["B19"].value * basementFinalSqft, 2)
        trimBasementCostTotal = trimBasementCostSqft + trimBasementCostLabor
        isBasementFinishedText = "TRUE"
        
        basementCostTotal = framingBasementCostSqft + electricalBasementCostSqft + plumbingBasementCostSqft + sheetrockBasementCostTotal + paintingBasementCostSqft + heatingBasementCostSqft + insulationBasementCostSqft + trimBasementCostTotal + concreteBasementCostTotal + foundatoinCost + excavationBasementCost + gravelBasementCost

    else:
        isBasementFinishedText = "FALSE"
        
        basementCostTotal = framingBasementCostSqft + heatingBasementCostSqft + insulationBasementCostSqft + concreteBasementCostTotal + foundatoinCost + excavationBasementCost + gravelBasementCost

    heatingGarageCostSqft = round(spreadsheet["B16"].value * garageFinalSqft, 2)    
    insulationGarageCostSqft = round(spreadsheet["B17"].value * garageFinalSqft, 2)
    concreteGarageCostSqft = round(spreadsheet["B20"].value * garageFinalSqft, 2)
    concreteGarageCostLabor = round(spreadsheet["B21"].value * garageFinalSqft, 2)
    concreteGarageCostTotal = concreteGarageCostSqft + concreteGarageCostLabor
    sheetrockGarageCostSqft = round(spreadsheet["B13"].value * garageFinalSqft, 2)
    sheetrockGarageCostLabor = round(spreadsheet["B14"].value * garageFinalSqft, 2)
    sheetrockGarageCostTotal = sheetrockGarageCostSqft + sheetrockGarageCostLabor    
    excavationGarageCost = round(spreadsheet["B23"].value * garageFinalSqft, 2)
    gravelGarageCost = round(spreadsheet["B24"].value * garageFinalSqft, 2)

    garageCostTotal = heatingGarageCostSqft + insulationGarageCostSqft + concreteGarageCostTotal + excavationGarageCost + gravelGarageCost

    if(doesExist == 1):
        totalOverhead = round((mainCostTotal + secondCostTotal + basementCostTotal + garageCostTotal + totalOtherCost) * 0.06, 2)
        totalCost = mainCostTotal + secondCostTotal + basementCostTotal + garageCostTotal + totalOverhead + totalOtherCost
    else:
        totalOverhead = round((mainCostTotal + basementCostTotal + garageCostTotal + totalOtherCost) * 0.06, 2)
        totalCost = mainCostTotal + basementCostTotal + garageCostTotal + totalOverhead + totalOtherCost
   
    
    calculationWindow = customtkinter.CTkToplevel()
    calculationWindow.title("Estimated Price")
    calculationWindow.geometry("650x250")
    calculationWindow.after(250, lambda: calculationWindow.iconbitmap('D:\Coding\Python\Liberty\LES.ico'))

    mainFrame = customtkinter.CTkScrollableFrame(calculationWindow)
    mainFrame.pack(fill = BOTH, expand = True)

    
    displayTotalCost = customtkinter.CTkLabel(mainFrame, text = "Total Cost: $" + str(totalCost), anchor="w").grid(row = 0, column = 0, sticky=W+E)
    displayTotalSqft = customtkinter.CTkLabel(mainFrame, text = "Total SqFt: " + str(finalSqft), anchor="w").grid(row = 1, column = 0, sticky=W+E)

    displayOverhead = customtkinter.CTkLabel(mainFrame, text = "Overhead Expenses: $" + str(totalOverhead), anchor="w").grid(row = 2, column = 1, sticky=W+E)
    displayPermit = customtkinter.CTkLabel(mainFrame, text = "Building Permit: $" + str(permitCost), anchor="w").grid(row = 3, column = 1, sticky=W+E)
    displayEngineering = customtkinter.CTkLabel(mainFrame, text = "Engineering: $" + str(engineeringCost), anchor="w").grid(row = 4, column = 1, sticky=W+E)
    displayTrusses = customtkinter.CTkLabel(mainFrame, text = "Trusses: $" + str(trussCostTotal), anchor="w").grid(row = 5, column = 1, sticky=W+E)
    displayRoofing = customtkinter.CTkLabel(mainFrame, text = "Roofing: $" + str(roofingCostTotal), anchor="w").grid(row = 6, column = 1, sticky=W+E)
    displayRoofingLabor = customtkinter.CTkLabel(mainFrame, text = "Labor: $" + str(roofingLaborCost), anchor="w").grid(row = 7, column = 2, sticky=W+E)
    displayRoofingMaterials = customtkinter.CTkLabel(mainFrame, text = "Materials: $" + str(roofingCostSqft), anchor="w").grid(row = 8, column = 2, sticky=W+E)
    displayBrick = customtkinter.CTkLabel(mainFrame, text = "Brick: $" + str(brickCostTotal), anchor="w").grid(row = 9, column = 1, sticky=W+E)
    displayBrickLabor = customtkinter.CTkLabel(mainFrame, text = "Labor: $" + str(brickCostLabor), anchor="w").grid(row = 10, column = 2, sticky=W+E)
    displayBrickMaterials = customtkinter.CTkLabel(mainFrame, text = "Materials: $" + str(brickCostSqft), anchor="w").grid(row = 11, column = 2, sticky=W+E)
    displaySiding = customtkinter.CTkLabel(mainFrame, text = "Siding: $" + str(sidingCostTotal), anchor="w").grid(row = 12, column = 1, sticky=W+E)
    displaySidingLabor = customtkinter.CTkLabel(mainFrame, text = "Labor: $" + str(sidingCostLabor), anchor="w").grid(row = 13, column = 2, sticky=W+E)
    displaySidingMaterials = customtkinter.CTkLabel(mainFrame, text = "Materials: $" + str(sidingCostSqft), anchor="w").grid(row = 14, column = 2, sticky=W+E)

    displayMainCost = customtkinter.CTkLabel(mainFrame, text = "Main Floor: $" + str(mainCostTotal), anchor="w").grid(row = 15, column = 1, sticky=W+E)
    displayMainSqft = customtkinter.CTkLabel(mainFrame, text = "SqFt: " + str(mainFinalSqft), anchor="w").grid(row = 16, column = 2, sticky=W+E)
    displayLumber = customtkinter.CTkLabel(mainFrame, text = "Lumber/SqFt: $" + str(lumberSqft), anchor="w").grid(row = 17, column = 2, sticky=W+E)
    displayFraming = customtkinter.CTkLabel(mainFrame, text = "Framing: $" + str(framingMainCostSqft), anchor="w").grid(row = 18, column = 2, sticky=W+E)
    displayElectrical = customtkinter.CTkLabel(mainFrame, text = "Electrical: $" + str(electricalMainCostSqft), anchor="w").grid(row = 19, column = 2, sticky=W+E)
    displayPlumbing = customtkinter.CTkLabel(mainFrame, text = "Plumbing: $" + str(plumbingMainCostSqft), anchor="w").grid(row = 20, column = 2, sticky=W+E)
    displaySheetrock = customtkinter.CTkLabel(mainFrame, text = "Sheetrock: $" + str(sheetrockMainCostTotal), anchor="w").grid(row = 21, column = 2, sticky=W+E)
    displaySheetrockLabor = customtkinter.CTkLabel(mainFrame, text = "Labor: $" + str(sheetrockMainCostLabor), anchor = "w").grid(row = 22, column = 3, sticky = W+E)
    displaySheetrockMaterials = customtkinter.CTkLabel(mainFrame, text = "Materials: $" + str(sheetrockMainCostSqft), anchor = "w").grid(row = 23, column = 3, sticky = W+E)
    displayPainting = customtkinter.CTkLabel(mainFrame, text = "Painting: $" + str(paintingMainCostSqft), anchor="w").grid(row = 24, column = 2, sticky=W+E)
    displayHeating = customtkinter.CTkLabel(mainFrame, text = "Heating: $" + str(heatingMainCostSqft), anchor="w").grid(row = 25, column = 2, sticky=W+E)
    displayInsulation = customtkinter.CTkLabel(mainFrame, text = "Insulation: $" + str(insulationMainCostSqft), anchor="w").grid(row = 26, column = 2, sticky=W+E)
    displayTrim = customtkinter.CTkLabel(mainFrame, text = "Trim: $" + str(trimMainCostTotal), anchor="w").grid(row = 27, column = 2, sticky=W+E)
    displayTrimLabor = customtkinter.CTkLabel(mainFrame, text = "Labor: $" + str(trimMainCostLabor), anchor="w").grid(row = 28, column = 3, sticky=W+E)
    displayTrimMaterials = customtkinter.CTkLabel(mainFrame, text = "Materials: $" + str(trimMainCostSqft), anchor="w").grid(row = 29, column = 3, sticky=W+E)

    if(doesExist == 1):
        displaySecondCost = customtkinter.CTkLabel(mainFrame, text = "Second Floor: $" + str(secondCostTotal), anchor="w").grid(row = 30, column = 1, sticky=W+E)
        displaySecondSqft = customtkinter.CTkLabel(mainFrame, text = "SqFt: " + str(secondFinalSqft), anchor="w").grid(row = 31, column = 2, sticky=W+E)
        displayLumber = customtkinter.CTkLabel(mainFrame, text = "Lumber/SqFt: $" + str(lumberSqft), anchor="w").grid(row = 32, column = 2, sticky=W+E)
        displayFraming = customtkinter.CTkLabel(mainFrame, text = "Framing: $" + str(framingSecondCostSqft), anchor="w").grid(row = 33, column = 2, sticky=W+E)
        displayElectrical = customtkinter.CTkLabel(mainFrame, text = "Electrical: $" + str(electricalSecondCostSqft), anchor="w").grid(row = 34, column = 2, sticky=W+E)
        displayPlumbing = customtkinter.CTkLabel(mainFrame, text = "Plumbing: $" + str(plumbingSecondCostSqft), anchor="w").grid(row = 35, column = 2, sticky=W+E)
        displaySheetrock = customtkinter.CTkLabel(mainFrame, text = "Sheetrock: $" + str(sheetrockSecondCostTotal), anchor="w").grid(row = 36, column = 2, sticky=W+E)
        displaySheetrockLabor = customtkinter.CTkLabel(mainFrame, text = "Labor: $" + str(sheetrockSecondCostLabor), anchor = "w").grid(row = 37, column = 3, sticky = W+E)
        displaySheetrockMaterials = customtkinter.CTkLabel(mainFrame, text = "Materials: $" + str(sheetrockSecondCostSqft), anchor = "w").grid(row = 38, column = 3, sticky = W+E)
        displayPainting = customtkinter.CTkLabel(mainFrame, text = "Painting: $" + str(paintingSecondCostSqft), anchor="w").grid(row = 39, column = 2, sticky=W+E)
        displayHeating = customtkinter.CTkLabel(mainFrame, text = "Heating: $" + str(heatingSecondCostSqft), anchor="w").grid(row = 40, column = 2, sticky=W+E)
        displayInsulation = customtkinter.CTkLabel(mainFrame, text = "Insulation: $" + str(insulationSecondCostSqft), anchor="w").grid(row = 41, column = 2, sticky=W+E)
        displayTrim = customtkinter.CTkLabel(mainFrame, text = "Trim: $"  + str(trimSecondCostTotal), anchor="w").grid(row = 42, column = 2, sticky=W+E)
        displayTrimLabor = customtkinter.CTkLabel(mainFrame, text = "Labor: $" + str(trimSecondCostLabor), anchor="w").grid(row = 43, column = 3, sticky=W+E)
        displayTrimMaterials = customtkinter.CTkLabel(mainFrame, text = "Materials: $" + str(trimSecondCostSqft), anchor="w").grid(row = 44, column = 3, sticky=W+E)

    displayBasementCost = customtkinter.CTkLabel(mainFrame, text = "Basement: $" + str(basementCostTotal), anchor="w").grid(row = 45, column = 1, sticky=W+E)
    displayBasementSqft = customtkinter.CTkLabel(mainFrame, text = "SqFt: " + str(basementFinalSqft), anchor="w").grid(row = 46, column = 2, sticky=W+E)
    displayFinishedBasement = customtkinter.CTkLabel(mainFrame, text = "Finished Basement: " + str(isBasementFinishedText), anchor="w").grid(row = 47, column = 2, sticky=W+E)
    
    if(isFinished == 1):
        displayElectrical = customtkinter.CTkLabel(mainFrame, text = "Electrical: $" + str(electricalBasementCostSqft), anchor="w").grid(row = 48, column = 3, sticky=W+E)
        displayPlumbing = customtkinter.CTkLabel(mainFrame, text = "Plumbing: $" + str(plumbingBasementCostSqft), anchor="w").grid(row = 49, column = 3, sticky=W+E)
        displaySheetrock = customtkinter.CTkLabel(mainFrame, text = "Sheetrock: $" + str(sheetrockBasementCostTotal), anchor="w").grid(row = 50, column = 3, sticky=W+E)
        displaySheetrockLabor = customtkinter.CTkLabel(mainFrame, text = "Labor: $" + str(sheetrockBasementCostLabor), anchor = "w").grid(row = 51, column = 4, sticky = W+E)
        displaySheetrockMaterials = customtkinter.CTkLabel(mainFrame, text = "Materials: $" + str(sheetrockBasementCostSqft), anchor = "w").grid(row = 52, column = 4, sticky = W+E)
        displayPainting = customtkinter.CTkLabel(mainFrame, text = "Painting: $" + str(paintingBasementCostSqft), anchor="w").grid(row = 53, column = 3, sticky=W+E)
        displayTrim = customtkinter.CTkLabel(mainFrame, text = "Trim: $" + str(trimBasementCostTotal), anchor="w").grid(row = 54, column = 3, sticky=W+E)
        displayTrimLabor = customtkinter.CTkLabel(mainFrame, text = "Labor: $" + str(trimBasementCostLabor), anchor="w").grid(row = 55, column = 4, sticky=W+E)
        displayTrimMaterials = customtkinter.CTkLabel(mainFrame, text = "Materials: $" + str(trimBasementCostSqft), anchor="w").grid(row = 56, column = 4, sticky=W+E)
        
    displayConcrete = customtkinter.CTkLabel(mainFrame, text = "Concrete: $" + str(concreteBasementCostTotal), anchor="w").grid(row = 57, column = 2, sticky=W+E)
    displayConcreteLabor = customtkinter.CTkLabel(mainFrame, text = "Labor: $" + str(concreteBasementCostLabor), anchor="w").grid(row = 58, column = 3, sticky=W+E)
    displayConcreteMaterials = customtkinter.CTkLabel(mainFrame, text = "Materials: $" + str(concreteBasementCostSqft), anchor="w").grid(row = 59, column = 3, sticky=W+E)
    displayFoundation = customtkinter.CTkLabel(mainFrame, text = "Foundation: $" + str(foundatoinCost), anchor="w").grid(row = 60, column = 2, sticky=W+E)
    displayExcavation = customtkinter.CTkLabel(mainFrame, text = "Excavation: $" + str(excavationBasementCost), anchor="w").grid(row = 61, column = 2, sticky=W+E)
    displayGravel = customtkinter.CTkLabel(mainFrame, text = "Gravel: $" + str(gravelBasementCost), anchor="w").grid(row = 62, column = 2, sticky=W+E)
    displayFraming = customtkinter.CTkLabel(mainFrame, text = "Framing: $" + str(framingBasementCostSqft), anchor="w").grid(row = 63, column = 2, sticky=W+E)
    displayHeating = customtkinter.CTkLabel(mainFrame, text = "Heating: $" + str(heatingBasementCostSqft), anchor="w").grid(row = 64, column = 2, sticky=W+E)
    displayInsulation = customtkinter.CTkLabel(mainFrame, text = "Insulation: $" + str(insulationBasementCostSqft), anchor="w").grid(row = 65, column = 2, sticky=W+E)
    
    displayGarageCost = customtkinter.CTkLabel(mainFrame, text = "Garage: $" + str(garageCostTotal), anchor="w").grid(row = 66, column = 1, sticky=W+E)
    displayGarageSqft = customtkinter.CTkLabel(mainFrame, text = "SqFt: " + str(garageFinalSqft), anchor="w").grid(row = 67, column = 2, sticky=W+E)
    displayLumber = customtkinter.CTkLabel(mainFrame, text = "Lumber/SqFt: $" + str(lumberSqft), anchor="w").grid(row = 68, column = 2, sticky=W+E)
    displaySheetrock = customtkinter.CTkLabel(mainFrame, text = "Sheetrock: $" + str(sheetrockGarageCostTotal), anchor="w").grid(row = 69, column = 2, sticky=W+E)
    displaySheetrockLabor = customtkinter.CTkLabel(mainFrame, text = "Labor: $" + str(sheetrockGarageCostLabor), anchor = "w").grid(row = 70, column = 3, sticky = W+E)
    displaySheetrockMaterials = customtkinter.CTkLabel(mainFrame, text = "Materials: $" + str(sheetrockGarageCostSqft), anchor = "w").grid(row = 71, column = 3, sticky = W+E)
    displayConcrete = customtkinter.CTkLabel(mainFrame, text = "Concrete: $" + str(concreteGarageCostTotal), anchor="w").grid(row = 72, column = 2, sticky=W+E)
    displayConcreteLabor = customtkinter.CTkLabel(mainFrame, text = "Labor: $" + str(concreteGarageCostLabor), anchor="w").grid(row = 73, column = 3, sticky=W+E)
    displayConcreteMaterials = customtkinter.CTkLabel(mainFrame, text = "Materials: $" + str(concreteGarageCostSqft), anchor="w").grid(row = 74, column = 3, sticky=W+E)
    displayExcavation = customtkinter.CTkLabel(mainFrame, text = "Excavation: $" + str(excavationBasementCost), anchor="w").grid(row = 75, column = 2, sticky=W+E)
    displayGravel = customtkinter.CTkLabel(mainFrame, text = "Gravel: $" + str(gravelGarageCost), anchor="w").grid(row = 76, column = 2, sticky=W+E)
    displayHeating = customtkinter.CTkLabel(mainFrame, text = "Heating: $" + str(heatingGarageCostSqft), anchor="w").grid(row = 77, column = 2, sticky=W+E)
    displayInsulation = customtkinter.CTkLabel(mainFrame, text = "Insulation: $" + str(insulationGarageCostSqft), anchor="w").grid(row = 78, column = 2, sticky=W+E)

#Labels
estimatedDate = customtkinter.CTkLabel(root, text = "Estimated Finish Date")
location = customtkinter.CTkLabel(root, text = "Location")

mainSqftLabel = customtkinter.CTkLabel(root, text = "Main Floor")
secondSqftLabel = customtkinter.CTkLabel(root, text = "Second Floor")
basementSqftLabel = customtkinter.CTkLabel(root, text = "Basement")
garageSqftLabel = customtkinter.CTkLabel(root, text = "Garage")
totalSqftLabel = customtkinter.CTkLabel(root, text = "Total")

addOnsLabel = customtkinter.CTkLabel(root, text = "Add Ons")

#Buttons
calculateButton = customtkinter.CTkButton(root, text = "Calculate Cost", command = calculationClick, state= DISABLED)

#Normal Entry Boxes
mainSqftEntry = customtkinter.CTkEntry(root)
mainSqftEntry.insert(0, "0")
secondSqftEntry = customtkinter.CTkEntry(root)
secondSqftEntry.insert(0, "0")
basementSqftEntry = customtkinter.CTkEntry(root)
basementSqftEntry.insert(0, "0")
garageSqftEntry = customtkinter.CTkEntry(root)
garageSqftEntry.insert(0, "0")

mainSqft = int(mainSqftEntry.get())
basementSqft = int(basementSqftEntry.get())
garageSqft = int(garageSqftEntry.get())

totalSqftOutput = customtkinter.CTkLabel(root, text = str(mainSqft+basementSqft+garageSqft))

#Dropdown Menu
locationSelected = StringVar()
locationOptions = [
    "Idaho Falls",
    "Ammon",
    "Iona",
    "Bonneville County"
]
locationDropdown = customtkinter.CTkOptionMenu(master=root, values=locationOptions, variable=locationSelected)
locationDropdown.set("Idaho Falls")

#Calendar Selection Menu
selectedDate = customtkinter.CTkEntry(root)

#Checkboxes
secondVar = IntVar()
secondCheck = customtkinter.CTkCheckBox(root, text = "Second Floor?", variable = secondVar, onvalue = 1, offvalue = 0, command = updateCheck)
finishedVar = IntVar()
finishedCheck = customtkinter.CTkCheckBox(root, text = "Finished Basement?", variable = finishedVar)

#Row one spacing and guide
estimatedDate.grid(row = 0, column = 1)
location.grid(row = 0, column = 2)

selectedDate.grid(row = 1, column = 1)
selectedDate.insert(0, "mm/dd/yyyy")
selectedDate.bind("<1>", datePicker)
locationDropdown.grid(row = 1, column = 2)

mainSqftLabel.grid(row = 2, column = 0)
totalSqftLabel.grid(row = 2, column = 3)

mainSqftEntry.grid(row = 3, column = 0)
totalSqftOutput.grid(row = 3, column = 3)
totalSqftOutput.after(1000, update)

secondCheck.grid(row = 4, column = 3)

basementSqftLabel.grid(row = 6, column = 0)
finishedCheck.grid(row = 6, column = 3)

basementSqftEntry.grid(row = 7, column = 0)

garageSqftLabel.grid(row = 8, column = 0)

garageSqftEntry.grid(row = 9, column = 0)

calculateButton.grid(row = 10, column = 1)

root.mainloop()
