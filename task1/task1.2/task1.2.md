# Task 1.2: Custom C++ Desktop Deployment Guide & Checklist (Visual Studio 2022 & HeatWave WiX v4)

This document details the complete step-by-step procedure, technical requirements, and screenshot evidence checklist for **Task 1.2 (Credit Tier)** of the **SWE40006 Deployment Portfolio**.

It demonstrates deploying your custom C++ desktop application (**`AlphtechDSP_2.0_App.exe`**) using Visual Studio 2022 and HeatWave WiX v4.

---

## 1. Task Objective & Context

* **Assignment Requirement:** *"Follow the WiX walkthrough and deploy your own C, C++, or C# desktop."*
* **Target Grade:** Credit (Tier 2 requirement).
* **Application Target:** **`AlphtechDSP_2.0_App.exe`** (Custom Win32 GDI+ Tube Amp Modelling Desktop Interface).
* **Core Concepts Demonstrated:**
  * Packaging custom C++ application binaries.
  * Custom directory creation (`C:\Program Files\Alphtech\AlphtechDSP 2.0.1`).
  * Creating Start Menu & Desktop shortcuts.
  * Windows Installed Apps product registration.

---

## 2. Step-by-Step Execution Guide (Visual Studio 2022 Workflow)

### Step 1: Open AlphtechDSP 2.0 Solution & Verify Build
1. Open your Visual Studio 2022 solution:
   `C:\Users\Admin\Documents\AlphtechDSP_2.0\AlphtechDSP_2.0.sln`
2. Build `AlphtechDSP_2.0_App` (**Ctrl + Shift + B**) in **x64 Debug** or **x64 Release**.
3. Confirm that `AlphtechDSP_2.0_App.exe` is generated in `x64\Debug\` (or `x64\Release\`).
> 📸 **Screenshot Opportunity (1.2_1.png):** Visual Studio IDE showing `AlphtechDSP_2.0_App` running cleanly.

---

### Step 2: Add WiX Installer Project (`WiXAlphtechDSP_2.0`)
1. In Solution Explorer, right-click **Solution 'AlphtechDSP_2.0'** $\rightarrow$ **Add** $\rightarrow$ **New Project**.
2. Search for `wix` and select:
   **`MSI Package (WiX v4)`** (from HeatWave).
3. Name the project: **`WiXAlphtechDSP_2.0`**.
4. Click **Create**.
5. Visual Studio will scaffold `Package.wxs`, `Folders.wxs`, and `ExampleComponents.wxs` inside `WiXAlphtechDSP_2.0`.
> 📸 **Screenshot Opportunity (1.2_2.png):** "Configure your new project" dialog naming the WiX project `WiXAlphtechDSP_2.0`.

---

### Step 3: Add Project Reference to AlphtechDSP_2.0_App
1. Right-click **Dependencies** (or **References**) in `WiXAlphtechDSP_2.0` $\rightarrow$ **Add Project Reference...**
2. Check the box next to **`AlphtechDSP_2.0_App`** and click **OK**.
> 📸 **Screenshot Opportunity (1.2_3.png):** Reference Manager dialog displaying `AlphtechDSP_2.0_App` checked.

---

### Step 4: Configure `AlphtechDSPWiX.wixproj`
Open `AlphtechDSPWiX.wixproj` in Visual Studio and configure the preprocessor variables:

```xml
<Project Sdk="WixToolset.Sdk/5.0.2">
  <PropertyGroup>
    <DefineConstants>
      AlphtechAppBin=..\x64\Debug;
      Manufacturer=Alphtech;
      ProductName=AlphtechDSP 2.0.1;
      ProductVersion=2.0.1;
    </DefineConstants>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="WixToolset.Heat" Version="5.0.2" />
    <PackageReference Include="WixToolset.UI.wixext" Version="5.0.2" />
  </ItemGroup>
</Project>
```

---

### Step 5: Configure Manifest Files (`Package.wxs`, `Folders.wxs`, `ExampleComponents.wxs`)

#### `Package.wxs`:
```xml
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs"
     xmlns:ui="http://wixtoolset.org/schemas/v4/wxs/ui">
  <Package Name="$(var.ProductName)"
           Manufacturer="$(var.Manufacturer)"
           Version="$(var.ProductVersion)"
           Scope="perMachine"
           UpgradeCode="{a839f123-4567-89ab-cdef-0123456789ab}">

    <!-- Prevent downgrade installation -->
    <MajorUpgrade DowngradeErrorMessage="A newer version of $(var.ProductName) is already installed." />

    <!-- Embed installation cabinet directly into MSI -->
    <MediaTemplate EmbedCab="yes" />

    <Feature Id="Main" Title="$(var.ProductName)">
      <ComponentGroupRef Id="AppFiles" />
    </Feature>

    <!-- Installer UI Wizard -->
    <ui:WixUI Id="WixUI_InstallDir" InstallDirectory="INSTALLFOLDER" />
  </Package>
</Wix>
```

#### `Folders.wxs`:
```xml
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
  <Fragment>
    <StandardDirectory Id="ProgramFiles64Folder">
      <Directory Id="ManufacturerFolder" Name="$(var.Manufacturer)">
        <Directory Id="INSTALLFOLDER" Name="$(var.ProductName)" />
      </Directory>
    </StandardDirectory>
    <StandardDirectory Id="ProgramMenuFolder" />
    <StandardDirectory Id="DesktopFolder" />
  </Fragment>
</Wix>
```

#### `ExampleComponents.wxs`:
```xml
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
  <Fragment>
    <ComponentGroup Id="AppFiles" Directory="INSTALLFOLDER">
      <Component Id="Cmp_AlphtechDSPApp" Guid="*">
        <File Id="File_AlphtechDSPApp" Source="$(var.AlphtechAppBin)\AlphtechDSP_2.0_App.exe" KeyPath="yes" />

        <!-- Start Menu Shortcut -->
        <Shortcut Name="$(var.ProductName)"
                  Directory="ProgramMenuFolder"
                  Advertise="yes"
                  WorkingDirectory="INSTALLFOLDER" />

        <!-- Desktop Shortcut -->
        <Shortcut Name="$(var.ProductName)"
                  Directory="DesktopFolder"
                  Advertise="yes"
                  WorkingDirectory="INSTALLFOLDER" />
      </Component>
    </ComponentGroup>
  </Fragment>
</Wix>
```
> 📸 **Screenshot Opportunity (1.2_4.png):** Visual Studio IDE displaying `Package.wxs` in the code editor and Solution Explorer on the right.

---

### Step 6: Build Solution in Visual Studio
1. Right-click `WiXAlphtechDSP_2.0` $\rightarrow$ **Build**.
2. In the Output window at the bottom, verify:
   `========== Build: 1 succeeded, 0 failed ==========`
3. Open folder: `WiXAlphtechDSP_2.0\bin\x64\Debug\en-US\` $\rightarrow$ verify **`WiXAlphtechDSP_2.0.msi`** exists!
> 📸 **Screenshot Opportunity (1.2_5.png):** Visual Studio Output window showing successful build and File Explorer showing `WiXAlphtechDSP_2.0.msi`.

---

### Step 7: Install, Verify & Missing Dependency Error (Motivation for Task 1.3)
1. **Execute Installer:** Double-click `WiXAlphtechDSP_2.0.msi` to run the setup wizard.
   > 📸 **Screenshot Opportunity (1.2_6.png):** Windows Installer setup wizard running for AlphtechDSP 2.0.1.
2. **Execute Installed Desktop Shortcut & Document System Error:** Run the newly installed application from the Desktop shortcut. Because only the standalone `.exe` was packaged without its shared DLL dependencies, Windows raises a missing DLL system error dialog (`The code execution cannot proceed because ... was not found`), directly demonstrating the real-world deployment problem that Task 1.3 solves.
   > 📸 **Screenshot Opportunity (1.2_7.png):** Desktop shortcut launch failure showing the missing DLL system error dialog.

