# Task 1.3: Multi-Component & Dual DLL Dependency Deployment Guide & Checklist (Visual Studio 2022 & HeatWave WiX v4)

This document details the complete step-by-step procedure, technical requirements, and screenshot evidence checklist for **Task 1.3 (Distinction Tier)** of the **SWE40006 Deployment Portfolio**.

It demonstrates deploying your custom C++ desktop application (**`AlphtechDSP_2.0_App.exe`**) together with its dual shared library dependencies (**`AlphtechDSP_2.0_Amp.dll`** and **`AlphtechDSP_2.0_Effects.dll`**) using Visual Studio 2022 and HeatWave WiX v4.

---

## 1. Task Objective & Context

* **Assignment Requirement:** *"Complete tasks 1.1 or 1.2 AND deploy an application with multiple DLLs or dependencies."*
* **Target Grade:** Distinction (Tier 3 requirement).
* **Application Targets:**
  1. `AlphtechDSP_2.0_App.exe` (Win32 GDI+ User Interface Executable)
  2. `AlphtechDSP_2.0_Amp.dll` (Vacuum Tube Preamp Overdrive & 3-Band Tone Stack EQ Engine Shared Dynamic Link Library)
  3. `AlphtechDSP_2.0_Effects.dll` (Stereo Ping-Pong Delay & Spatial Ambience DSP Engine Shared Dynamic Link Library)
* **Core Concepts & Error Eradication Demonstrated:**
  * Multi-component WiX manifest authoring for multiple dynamic-link libraries.
  * Eradicating missing DLL System Errors (`AlphtechDSP_2.0_Amp.dll was not found` and `AlphtechDSP_2.0_Effects.dll was not found`).
  * Atomic multi-file payload deployment to `C:\Program Files\Alphtech\AlphtechDSP 2.0.1`.

---

## 2. Step-by-Step Execution Guide (Visual Studio 2022 Workflow)

### Step 1: Open AlphtechDSP 2.0 Solution & Verify Binaries
1. Open your Visual Studio 2022 solution:
   `C:\Users\Admin\Documents\AlphtechDSP_2.0\AlphtechDSP_2.0.sln`
2. Build the solution (**Ctrl + Shift + B**) in **x64 Debug** (or x64 Release).
3. Confirm that `AlphtechDSP_2.0_App.exe`, `AlphtechDSP_2.0_Amp.dll`, and `AlphtechDSP_2.0_Effects.dll` exist inside `x64\Debug\`.
> 📸 **Screenshot Opportunity (1.3_2.png):** File Explorer navigated to `Documents > AlphtechDSP_2.0 > x64 > Debug` with `AlphtechDSP_2.0_App.exe`, `AlphtechDSP_2.0_Amp.dll`, and `AlphtechDSP_2.0_Effects.dll` selected/highlighted.

---

### Step 2: Configure Project References in `WiXAlphtechDSP_2.0`
1. In Solution Explorer, expand the `WiXAlphtechDSP_2.0` WiX project.
2. Right-click **Dependencies** (or **References**) $\rightarrow$ **Add Project Reference...**
3. Ensure checkboxes are checked for all three core projects:
   - `AlphtechDSP_2.0_App`
   - `AlphtechDSP_2.0_Amp`
   - `AlphtechDSP_2.0_Effects`
> 📸 **Screenshot Opportunity (1.3_1.png):** Visual Studio Reference Manager dialog displaying all three project references checked (`AlphtechDSP_2.0_App`, `AlphtechDSP_2.0_Amp`, and `AlphtechDSP_2.0_Effects`).

---

### Step 3: Configure `WiXAlphtechDSP_2.0.wixproj`
Verify that `WiXAlphtechDSP_2.0.wixproj` contains the preprocessor variable definitions and project references:

```xml
<Project Sdk="WixToolset.Sdk/5.0.2">
  <PropertyGroup>
    <DefineConstants>AlphtechDSP2AppBin=..\x64\Debug;Manufacturer=Alphtech;ProductName=AlphtechDSP 2.0.1;ProductVersion=2.0.1</DefineConstants>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="WixToolset.Heat" Version="5.0.2" />
    <PackageReference Include="WixToolset.UI.wixext" Version="5.0.2" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="..\AlphtechDSP_2.0_Amp\AlphtechDSP_2.0_Amp.vcxproj" />
    <ProjectReference Include="..\AlphtechDSP_2.0_Effects\AlphtechDSP_2.0_Effects.vcxproj" />
    <ProjectReference Include="..\AlphtechDSP_2.0_App\AlphtechDSP_2.0_App.vcxproj" />
  </ItemGroup>
</Project>
```

---

### Step 4: Update Manifest Files (`Package.wxs`, `Folders.wxs`, `ExampleComponents.wxs`)

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

#### `ExampleComponents.wxs` (Multi-Component Configuration):
```xml
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
  <Fragment>
    <ComponentGroup Id="AppFiles" Directory="INSTALLFOLDER">
      
      <!-- Primary User Interface Executable -->
      <Component Id="Cmp_AlphtechDSP2App" Guid="*">
        <File Id="File_AlphtechDSP2App" Source="$(var.AlphtechDSP2AppBin)\AlphtechDSP_2.0_App.exe" KeyPath="yes" />

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

      <!-- Multi-DLL Dependency 1: Tube Preamp & Tone Stack Overdrive Engine -->
      <Component Id="Cmp_AlphtechDSP_2.0_AmpDll" Guid="*">
        <File Id="File_AlphtechDSP_2.0_AmpDll" Source="$(var.AlphtechDSP2AppBin)\AlphtechDSP_2.0_Amp.dll" KeyPath="yes" />
      </Component>

      <!-- Multi-DLL Dependency 2: Stereo Delay & Spatial Ambience DSP Engine -->
      <Component Id="Cmp_AlphtechDSP_2.0_EffectsDll" Guid="*">
        <File Id="File_AlphtechDSP_2.0_EffectsDll" Source="$(var.AlphtechDSP2AppBin)\AlphtechDSP_2.0_Effects.dll" KeyPath="yes" />
      </Component>

    </ComponentGroup>
  </Fragment>
</Wix>
```
> 📸 **Screenshot Opportunity (1.3_3.png):** Visual Studio code editor displaying `ExampleComponents.wxs` with both the `.exe` and the two `.dll` components (`AlphtechDSP_2.0_Amp.dll` and `AlphtechDSP_2.0_Effects.dll`).

---

### Step 5: Build Solution in Visual Studio
1. In Solution Explorer, right-click `WiXAlphtechDSP_2.0` $\rightarrow$ **Build** (**Ctrl + Shift + B**).
2. In the Output window at the bottom, verify:
   `========== Build: 4 succeeded, 0 failed ==========`
3. Open folder: `WiXAlphtechDSP_2.0\bin\x64\Debug\en-US\` $\rightarrow$ verify **`WiXAlphtechDSP_2.0.msi`** exists!
> 📸 **Screenshot Opportunity (1.3_4.png):** Visual Studio Output window showing successful build on the left and File Explorer showing `WiXAlphtechDSP_2.0.msi` on the right.

---

### Step 6: Install, Verify & Eradicate System Errors
1. **Execute Installer:** Double-click `WiXAlphtechDSP_2.0.msi` to run the setup wizard.
2. **Verify Multi-Payload Installation:** Open File Explorer to `C:\Program Files\Alphtech\AlphtechDSP 2.0.1\` and confirm **all three files** (`AlphtechDSP_2.0_App.exe`, `AlphtechDSP_2.0_Amp.dll`, and `AlphtechDSP_2.0_Effects.dll`) are deployed together.
3. **Execute Deployed App & Verify Error Eradication:** Launch `AlphtechDSP_2.0_App.exe` directly from `Program Files`. The application dynamically binds both `AlphtechDSP_2.0_Amp.dll` and `AlphtechDSP_2.0_Effects.dll` with zero missing DLL dialogs, and the dark-mode GDI+ Tube Amp UI opens live!
> 📸 **Screenshot Opportunity (1.3_5.png):** File Explorer showing `C:\Program Files\Alphtech\AlphtechDSP 2.0.1\` with the executable and both DLLs present, with the live `AlphtechDSP 2.0.1` interface running in the foreground.
