# Task 1.1: Walkthrough Desktop Deployment Guide & Checklist (Visual Studio 2022 & HeatWave WiX v4)

This document details the complete step-by-step procedure, technical requirements, and screenshot evidence checklist for **Task 1.1 (Pass Tier)** of the **SWE40006 Deployment Portfolio**. 

It directly integrates:
1. The **SWE40006 Unit Walkthrough Guide (`WiX walkthrough.pdf`)** (Core requirements & architecture).
2. The **Tutor-Provided Video Tutorial (`https://www.youtube.com/watch?v=8xW7ooTMtjM`)** (Modern Visual Studio 2022 + HeatWave WiX v4 workflow).

---

## 1. Task Objective & Context

* **Assignment Requirement:** *"Follow the WiX walkthrough and deploy a sample desktop."*
* **Target Grade:** Pass (Tier 1 baseline required before advancing to Tasks 1.2, 1.3, and 1.4).
* **Workflow:** Integrated Visual Studio 2022 IDE workflow with the official **HeatWave for VS2022** extension, NuGet package integration (`WixToolset.UI.wixext`), and standard MSI compilation.

---

## 2. Step-by-Step Execution Guide (Following the Tutor's Video)

### Step 1: Install WiX Toolkit & HeatWave for Visual Studio 2022
1. Open a command prompt or PowerShell and install the WiX Toolkit globally via the .NET CLI:
   ```cmd
   dotnet nuget add source https://api.nuget.org/v3/index.json --name nuget.org
   dotnet nuget list source
   dotnet tool install --global wix
   ```
2. Open **Visual Studio 2022**.
3. Go to the top menu: **Extensions** $\rightarrow$ **Manage Extensions**.
4. In the search box, type: **`HeatWave for VS2022`**.
5. Click **Download**, then close Visual Studio to allow the VSIX installer to complete.
6. Reopen Visual Studio once installed.
> 📸 **Screenshot Opportunity (Figure 1.1):** HeatWave extension installed in Visual Studio Extensions Manager.

---

### Step 2: Open Solution & Verify SampleApp (Video: Project Setup)
1. Open your sample solution:
   `C:\Users\Admin\Documents\SWE40006\task1\task1.1\SampleApp\SampleApp.sln`
2. Ensure `SampleApp.cpp` contains the console pause (`std::cin.get();`):
   ```cpp
   #include <iostream>

   int main()
   {
       std::cout << "Hello World!\n";
       std::cin.get();
       return 0;
   }
   ```
3. Build `SampleApp` (**Ctrl + Shift + B**) and verify `Build: 1 succeeded`.
> 📸 **Screenshot Opportunity (Figure 1.2):** Visual Studio Solution Explorer showing the `SampleApp` project compiled.

---

### Step 3: Add WiX MSI Package Project (Video: Adding Installer Project)
1. In Solution Explorer, right-click **Solution 'SampleApp'** $\rightarrow$ **Add** $\rightarrow$ **New Project**.
2. Search for `wix` and select:
   **`MSI Package (WiX v4)`** (from HeatWave).
3. Name the project: **`SampleInstaller`** (or `WiXExample`).
4. Click **Create**.
5. Visual Studio will now scaffold the WiX project containing `Package.wxs` right inside your Solution Explorer!

---

### Step 4: Add Project Reference to SampleApp (Video: Reference Linking)
1. In your new `SampleInstaller` project, right-click **Dependencies** (or **References**) $\rightarrow$ **Add Project Reference...**
2. Check the box next to **`SampleApp`** and click **OK**.
3. This links the build outputs so the installer can package the executable.
> 📸 **Screenshot Opportunity (Figure 1.3):** Solution Explorer showing both `SampleApp` and `SampleInstaller` side-by-side with reference linked.

---

### Step 5: (Optional/Bonus) Add WiX UI Extension via NuGet (Video: Installer Wizard GUI)
In the video tutorial, the tutor installs the WiX UI package so the installer gets standard wizard dialogs (Welcome, Next, Finish):
1. Right-click the `SampleInstaller` project $\rightarrow$ **Manage NuGet Packages...**
2. In the **Browse** tab, search for: **`WixToolset.UI.wixext`**
3. Click **Install**.

---

### Step 6: Configure `Package.wxs` (Video: Authoring Manifest)
Double-click `Package.wxs` inside your `SampleInstaller` project in Visual Studio. Ensure its content specifies your details and points to `SampleApp.exe`:

```xml
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs"
     xmlns:ui="http://wixtoolset.org/schemas/v4/wxs/ui">
  <Package Name="Sample Desktop Application"
           Manufacturer="ICT Student"
           Version="1.0.0.0"
           UpgradeCode="d24e6a8b-1123-4c55-89fa-123456789abc"
           Scope="perMachine">

    <!-- Prevent downgrade installation -->
    <MajorUpgrade DowngradeErrorMessage="A newer version of [ProductName] is already installed." />

    <!-- Embed installation cabinet directly into the MSI (Walkthrough Page 9) -->
    <MediaTemplate EmbedCab="yes" />

    <!-- Optional: Wizard UI (From Video Tutorial) -->
    <ui:WixUI Id="WixUI_Minimal" />

    <!-- Install Directory: C:\Program Files\SampleDesktopApp -->
    <StandardDirectory Id="ProgramFiles64Folder">
      <Directory Id="INSTALLFOLDER" Name="SampleDesktopApp">
        <Component Id="MainExecutableComponent" Guid="a1b2c3d4-e5f6-7890-abcd-ef1234567890">
          <File Id="SampleAppExe" Source="..\SampleApp\x64\Debug\SampleApp.exe" KeyPath="yes" />
        </Component>
      </Directory>
    </StandardDirectory>

    <!-- Installation Feature -->
    <Feature Id="MainFeature" Title="Sample App Feature" Level="1">
      <ComponentRef Id="MainExecutableComponent" />
    </Feature>
  </Package>
</Wix>
```
*(Note: If you did not add the NuGet UI package, simply omit `xmlns:ui` and `<ui:WixUI Id="WixUI_Minimal" />`).*
> 📸 **Screenshot Opportunity (Figure 1.4):** Visual Studio editor displaying `Package.wxs`.

---

### Step 7: Build Solution in Visual Studio (Video: Compilation)
1. In Solution Explorer, right-click `SampleInstaller` $\rightarrow$ click **Build**.
2. In the Output window at the bottom, verify:
   `========== Build: 1 succeeded, 0 failed ==========`
3. Right-click `SampleInstaller` $\rightarrow$ **Open Folder in File Explorer**.
4. Go into `bin\x64\Debug` (or `bin\Debug`) $\rightarrow$ verify **`SampleInstaller.msi`** exists!
> 📸 **Screenshot Opportunity (Figure 1.5):** Visual Studio Output window showing successful build and File Explorer showing the `.msi` file.

---

### Step 8: Install, Verify & Uninstall (Lifecycle Testing)
1. **Execute Installer:** Double-click `SampleInstaller.msi` to run the setup wizard.
   > 📸 **Screenshot Opportunity (Figure 1.6):** Windows Installer setup dialog running.
2. **Verify File Placement:** Open File Explorer to `C:\Program Files\SampleDesktopApp` and verify `SampleApp.exe` is installed.
   > 📸 **Screenshot Opportunity (Figure 1.7):** Explorer showing installed executable in `Program Files`.
3. **Execute Deployed App:** Run `SampleApp.exe` directly from `C:\Program Files\SampleDesktopApp`. Verify it runs and pauses.
   > 📸 **Screenshot Opportunity (Figure 1.8):** Running console app alongside the `Program Files` window.
4. **Verify Windows Registry / Installed Apps:** Open Windows **Settings > Apps > Installed apps** and locate `Sample Desktop Application`.
   > 📸 **Screenshot Opportunity (Figure 1.9):** Windows Settings showing registered product with version `1.0.0.0`.
5. **Uninstall Verification:** Uninstall via Windows Settings or right-click `.msi` $\rightarrow$ Uninstall. Verify that `C:\Program Files\SampleDesktopApp` is completely removed.
   > 📸 **Screenshot Opportunity (Figure 1.10):** Clean folder removal post-uninstall.

