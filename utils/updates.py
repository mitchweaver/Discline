from utils.globals import term

def check_for_updates():
    try:# git pull at start as to automatically update to master repo
        from subprocess import Popen,PIPE
        print(term.green + "Checking for updates..." + term.normal)
        process = Popen(["git", "pull"], stdout=PIPE)
        output = process.communicate()[0].decode('utf-8').strip()

        if output != "Already up to date.":
            print("Updates downloaded! Please restart.")
            print("\n \n")



            # this is causing problems for some people...
            # quit()
        else:
            print("Already up to date!" + "\n")
    except KeyboardInterrupt: print("Call to cancel update received, skipping.")
    except SystemExit: pass
    except OSError: # (file not found)
        # They must not have git installed, no automatic updates for them!
        print(term.red + "Error fetching automatic updates! Do you \
              have git installed?" + term.normal)
    except:
        print(term.red + "Unkown error occurred during retrieval \
              of updates." + term.normal)
