import subprocess
import os
import git
import os

available_install_modules = [['ImageSorter','https://github.com/KJM-Code/ImageSorter.git','ImageSorter'], #Name, Repository, Directory Name
                             ['Users','https://github.com/KJM-Code/module_hw_user.git','users']
                     ]
working_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(working_path)

print('WP',working_path)

def get_available_update_modules():
    available_update_modules = []
    for module in os.listdir('modules/'):
        if os.path.isdir(f'modules/{module}/.git/'):
            available_update_modules.append(module)
    return available_update_modules

def run_module_setup(path,setup_file='setup.py'):
    if os.path.isfile(os.path.join(path,setup_file)):
        subprocess.run([f'python',os.path.join(path,setup_file)],check=True)


user_selection = None
available_options = ['Install Modules','Update Modules','Update Homeweb']



while True:
    while True:
        print('\n')
        print("*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*")
        print("Homeweb Installation - Modules & More")
        print("\n")
        print("Input 'q' to quit.")
        print(f"Please select an option (1-{len(available_options)}):")
        for opt_indx, option in enumerate(available_options):
            print(f"{opt_indx + 1}) {option}")
        try:
            user_selection = input(">> ")
            if user_selection in ['q','quit']:
                break
            user_selection = int(user_selection)
            user_selection = available_options[user_selection-1]
            break
        except:
            print("\nInvalid selection. Please select one of the available options. (EG: \"1\")")
    if user_selection in ['q', 'quit']:
        break




    if user_selection == 'Install Modules':
        available_update_modules = get_available_update_modules()
        while True:
            print("\nSelect the following module to install:")
            print('1) Install All Modules')
            for mod_indx, module in enumerate(available_install_modules):
                print(f"{mod_indx + 2}) {module[0]} {'[Installed]' if module[2] in available_update_modules else ''}")
            try:
                moduleSelection = input(">> ")
                if moduleSelection.lower() in ['quit', 'q']:
                    break
                moduleSelection = int(moduleSelection)
                if moduleSelection == 1:
                    for available_module in available_install_modules:
                        git.Repo.clone_from(available_module[1], os.path.join(working_path,'modules',available_module[2]))
                        run_module_setup(os.path.join(working_path,'modules',available_module[2]))
                        subprocess.run(
                            ['pip', 'install', '-r', os.path.join(working_path, 'modules','available_module[2]','requirements.txt')],
                            check=True)

                else:
                    git.Repo.clone_from(available_install_modules[moduleSelection-2][1],os.path.join(working_path,'modules',available_install_modules[moduleSelection-2][2]))
                    subprocess.run(
                        ['pip', 'install', '-r', os.path.join(working_path, 'modules',available_install_modules[moduleSelection-2][2], 'requirements.txt')],
                        check=True)
                    run_module_setup(os.path.join(working_path,'modules',available_install_modules[moduleSelection-2][2]))
                break
            except Exception as e:
                print("\nInvalid selection.")
                print(e)

    elif user_selection == 'Update Modules': #Only show available modules with .git directories
        available_update_modules = get_available_update_modules()
        if len(available_update_modules) > 0:
            while True:
                try:
                    print("Select the following module to update:")
                    print('1) Update All Modules')
                    for mod_indx, update_module in enumerate(available_update_modules):
                        print(f"{mod_indx + 2}) {update_module}")
                    moduleSelection = input(">> ")
                    if moduleSelection.lower() in ['quit','q']:
                        break
                    moduleSelection = int(moduleSelection)
                    if moduleSelection == 0:
                        for available_module in available_update_modules:
                            currModulePath = os.path.join(working_path, 'modules',available_module)
                            print("\nUpdating", currModulePath)
                            repo = git.Repo(currModulePath)
                            repo.remotes.origin.pull()
                            if os.path.isfile(os.path.join(working_path,currModulePath, 'requirements.txt')):
                                print("Installing Dependencies...")
                                subprocess.run(
                                    ['pip', 'install', '-r', os.path.join(working_path,currModulePath, 'requirements.txt')],
                                    check=True)
                                run_module_setup(os.path.join(working_path,currModulePath))
                                print("Dependencies Installed Correctly.")


                    else:
                        currModulePath = os.path.join(working_path,'modules',available_update_modules[moduleSelection-2])
                        print("\nUpdating",currModulePath)
                        repo = git.Repo(currModulePath)
                        repo.remotes.origin.pull()

                        if os.path.isfile(os.path.join(working_path,currModulePath,'requirements.txt')):
                            print("Installing Dependencies...")
                            subprocess.run(['pip', 'install', '-r', os.path.join(working_path,currModulePath,'requirements.txt')], check=True)
                            run_module_setup(os.path.join(working_path,currModulePath))
                            print("Dependencies Installed Correctly.")



                    break
                except Exception as e:
                    print("\nInvalid selection.")
                    print(e)
                    raise e
        else:
            print("No modules available to update.")
    elif user_selection == 'Update Homeweb':
        currModulePath = f''
        print("\nUpdating Homeweb")
        repo = git.Repo(os.path.join(working_path,currModulePath))
        repo.remotes.origin.pull()
        currentCommit = repo.head.commit

        if os.path.isfile(os.path.join(working_path,currModulePath, 'requirements.txt')):
            print("Installing Dependencies...")
            subprocess.run(['pip', 'install', '-r', os.path.join(working_path,currModulePath, 'requirements.txt')], check=True)

        if currentCommit != repo.head.commit:
            print("Updates to Homeweb have been made.")

