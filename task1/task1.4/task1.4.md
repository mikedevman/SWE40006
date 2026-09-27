# Task 1.4: Universal Windows App Packaging & Microsoft Store Deployment Guide (Visual Studio 2022 & Microsoft Store)

This document details the complete step-by-step procedure, technical requirements, and screenshot evidence guide for **Task 1.4 (High Distinction Tier)** of the **SWE40006 Deployment Portfolio**.

It strictly follows the official unit walkthrough (**`WiX walkthrough (updated 2026).pdf`**, Part 6: *Universal Windows App Packaging - Publish app to Microsoft Store*), deploying your custom C++ desktop application (**`AlphtechDSP_2.0_App.exe`**) and its dual shared library dependencies (**`AlphtechDSP_2.0_Amp.dll`** and **`AlphtechDSP_2.0_Effects.dll`**) into a modern sandboxed **MSIX / Universal Windows package** using Visual Studio 2022 and the **Windows Application Packaging Project (WAPP)**, and publishing directly to the **Microsoft Store** via Microsoft Partner Center.

---

## 1. Task Objective & Context

* **Assignment Requirement:** *"Complete 1.3 AND deploy the application to the Microsoft Store for public access/download OR explain in detail how to deploy to the Microsoft Store."*
* **Target Grade:** High Distinction (Tier 4 requirement).
* **Application Targets:**
  1. `AlphtechDSP_2.0_App.exe` (Win32 GDI+ User Interface Executable)
  2. `AlphtechDSP_2.0_Amp.dll` (Overdrive & Tone Stack EQ Shared Library Dependency)
  3. `AlphtechDSP_2.0_Effects.dll` (Delay & DSP Modulation Shared Library Dependency)
  4. `AlphtechDSP_Package` (Windows Application Packaging Project generating `.msixupload` / `.msixbundle`)
* **Core Concepts Demonstrated:**
  * Modern Windows App Packaging architecture (MSIX containerization).
  * Windows Application Packaging Project (WAPP) configuration in Visual Studio 2022.
  * Registering and managing a Microsoft Store Developer account in Microsoft Partner Center.
  * Reserving a globally unique product name in the Microsoft Store.
  * Packaging and generating an optimized Store upload package (`.msixupload` bundle).
  * Ingestion, Store listing metadata, IARC age certification, and submission for certification.

---

## 2. Step-by-Step Execution Guide (Following Walkthrough Part 6)

### Step 1: Create Microsoft Store Developer Account
*(Following Walkthrough Section 6, Step 1 & Pages 8–9)*
1. Go to the [Microsoft Store Developer Center](https://storedeveloper.microsoft.com/onboarding).
2. Sign up / sign in with your Microsoft Account.
3. Select **Individual developer** account type and complete verification.
> 📸 **Screenshot Opportunity (1.4_1.png):** Browser window showing account setup / registration completion in Microsoft Store Developer / Partner Center.

---

### Step 2: Reserve App Name in Microsoft Partner Center
*(Following Walkthrough Section 6, Pages 9–11)*
1. In [Microsoft Partner Center](https://partner.microsoft.com/dashboard), navigate to **Apps and games** $\rightarrow$ **Overview**.
2. Click **New product** $\rightarrow$ choose **MSIX or PWA app**.
3. In the reservation screen, enter your unique app name: e.g. `AlphtechDSP` (or `AlphtechDSP2026`).
4. Click **Check availability**, then click **Reserve product name**.
5. Once reserved, verify your app dashboard appears displaying **Product release: In draft**.
> 📸 **Screenshot Opportunity (1.4_2.png):** Partner Center dashboard showing your reserved app name and submission status in "In draft" (matching PDF Page 11).

---

### Step 3: Add Windows Application Packaging Project in Visual Studio
*(Following Walkthrough Section 6, Steps 2–3 & Pages 11–13)*
1. Open your Visual Studio 2022 solution:
   `C:\Users\Admin\Documents\AlphtechDSP_2.0\AlphtechDSP_2.0.sln`
2. In Solution Explorer, right-click **Solution 'AlphtechDSP_2.0'** $\rightarrow$ **Add** $\rightarrow$ **New Project...**
3. In the template search box, filter by **Visual C#** / **C++** and **UWP**, then select **Windows Application Packaging Project**.
4. Name the project: **`AlphtechDSP_Package`**.
5. Click **OK** / **Create**.
6. When prompted for target Windows versions, accept the default values (Windows 10, version 2004 / 19041 or higher).
> 📸 **Screenshot Opportunity (1.4_3.png):** Visual Studio Solution Explorer showing the newly created `AlphtechDSP_Package` project.

---

### Step 4: Add Application Project Reference
*(Following Walkthrough Section 6, Step 4 & Pages 13–14)*
1. In `AlphtechDSP_Package`, expand **Dependencies** (or **Applications**).
2. Right-click **Dependencies** $\rightarrow$ **Add Project Reference...**
3. Check the box next to **`AlphtechDSP_2.0_App`** and click **OK**.
4. Right-click `AlphtechDSP_2.0_App` under Applications and ensure it is designated as **Set as Entry Point** (bold text).
5. The packaging project automatically harvests `AlphtechDSP_2.0_App.exe` and its project dependencies (`AlphtechDSP_2.0_Amp.dll` and `AlphtechDSP_2.0_Effects.dll`).
> 📸 **Screenshot Opportunity (1.4_4.png):** Reference Manager dialog showing `AlphtechDSP_2.0_App` checked (matching PDF Page 14).

---

### Step 5: Launch Create App Packages Wizard
*(Following Walkthrough Section 6, Steps 5–6 & Pages 14–15)*
1. Right-click the `AlphtechDSP_Package` project in Solution Explorer $\rightarrow$ select **Publish** $\rightarrow$ **Create App Packages...**
2. In the **Select distribution method** dialog:
   * Select **"Microsoft Store under a new app name"**.
   * Click **Next**.
> 📸 **Screenshot Opportunity (1.4_5.png):** "Select distribution method" wizard showing "Microsoft Store under a new app name" selected (matching PDF Page 15).

---

### Step 6: Link Microsoft Account & Select Reserved App Name
*(Following Walkthrough Section 6, Step 7 & Page 16)*
1. Sign in with the Microsoft account associated with your registered Partner Center Developer profile.
2. Click **Refresh**. Visual Studio queries the Store API and displays your reserved app name from Step 2.
3. Select your reserved app name (e.g. `AlphtechDSP`).
4. Click **Next**.
> 📸 **Screenshot Opportunity (1.4_6.png):** "Select an app name" wizard showing your signed-in Microsoft account and the reserved app name selected (matching PDF Page 16).

---

### Step 7: Configure Target Architectures & Build Package
*(Following Walkthrough Section 6, Steps 8–9 & Pages 17–18)*
1. In the **Select and configure packages** screen:
   * **Output location:** default `AppPackages\AlphtechDSP_Package\`.
   * **Version:** `1.0.0.0` (or `2.0.1.0`).
   * **Generate app bundle:** Select **Always**.
   * **Architecture configuration:**
     * Uncheck **Neutral**.
     * Check **x64** (select **Release (x64)**).
     * Leave ARM / ARM64 unchecked.
2. Click **Create**.
3. Visual Studio compiles the C++ binaries, harvests all dependencies, builds the MSIX container, and packages it into an official `.msixupload` bundle.
4. When finished, the **Finished creating package** screen confirms success.
> 📸 **Screenshot Opportunity (1.4_7.png):** "Finished creating package" dialog displaying the output location and package details (matching PDF Page 18).

---

### Step 8: Upload Package to Microsoft Partner Center
*(Following Walkthrough Section 6, Steps 10–13 & Pages 18–20)*
1. Open the output folder: navigate to `AppPackages\AlphtechDSP_Package\...` and locate the generated **`.msixupload`** file (e.g. `AlphtechDSP_Package_1.0.0.0_x64.msixupload`).
2. Return to [Microsoft Partner Center](https://partner.microsoft.com/dashboard) and click your app submission draft.
3. Under **Submission 1**, click **Packages** (PDF Page 19).
4. Drag and drop your `.msixupload` file into the upload dropzone (PDF Page 20).
5. Partner Center validates package structure, capabilities (`runFullTrust`), and architecture.
6. Click **Save**.
> 📸 **Screenshot Opportunity (1.4_8.png):** Partner Center "Packages" page showing your uploaded `.msixupload` package validated and saved.

---

### Step 9: Complete Store Listing & Final Submission
*(Following Walkthrough Section 6, Step 14 & Page 20)*
Complete all remaining submission sections in Partner Center:
1. **Pricing and availability:** Set to **Free**, select all markets worldwide.
2. **Properties & Age Ratings:** Select Category *Music / Audio Production*, complete the short IARC age rating questionnaire.
3. **Store listings:** Fill in description, keywords, app logo, and desktop UI screenshot.
4. Once all sections show green checkmarks, click **Submit for certification**.
> 📸 **Screenshot Opportunity (1.4_9.png):** Submission overview page showing all submission sections completed and ready for certification (matching PDF Page 20).
