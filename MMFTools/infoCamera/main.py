def attachInfo(kwargs, type):
    import hou

    obj = hou.node("/obj")
    parm = kwargs['parms'][0]
    parms = kwargs['parms']
    parmnode = ".:" + parm.node().name() + ":."
    parmname = parm.description()

    if len(parms)==1:
        parmpath = parm.path()
        parmitem = parm.name()
    else:
        parmitem = parm.name()[:-1]

    child = obj.children()

    names = []
    for a in child: names.append(a.path())

    infonodes = [node for node in names if "Info_Camera" in node]

    if len(infonodes)==0:
        hou.ui.displayMessage("Seems like you don't have any info nodes in you Houdini scene. Make sure you have at least one to add the information.")

    elif len(infonodes)>0:
        if len(infonodes)==1:
            textpath = infonodes[0]
        else:
            try:
                selection = hou.ui.selectFromList(infonodes, height=1)[0]
            except:
                exit()
            textpath = infonodes[selection]

        if len(parms)==1:
            textmsg = hou.node(textpath).parm(type)
            currtextmsg = textmsg.rawValue()

            checkparm = parm.eval()
            decimals ='ch("decimals")'
            if isinstance(checkparm, float):
                parm = parmname + " ({0})".format(parmitem) + ': ' + '`ftrim(round(chs("{1}")*pow(10,{0}))/pow(10,{0}))`'.format(decimals, parmpath)
            else:
                parm = parmname + " ({0})".format(parmitem) + ': ' + '`chs("{0}")`'.format(parmpath)

            if type == "text_meta":
                if currtextmsg == "":
                    finalmsg = parm
                else:
                    finalmsg = currtextmsg + "\n" + parm
            else:
                if parmnode in currtextmsg:
                    corrected = currtextmsg.split(parmnode)
                    corrected.insert(1, parmnode)
                    corrected.insert(2, "\n" + parm)

                    finalmsg = "".join(corrected)
                else:
                    finalmsg = currtextmsg + "\n\n" + parmnode + "\n" + parm
        else:
            textmsg = hou.node(textpath).parm(type)
            currtextmsg = textmsg.rawValue()
            msg = []

            for p in parms:
                checkparm = p.eval()
                parmpath = p.path()
                decimals ='ch("decimals")'
                if isinstance(checkparm, float):
                    msg.append('`ftrim(round(chs("{1}")*pow(10,{0}))/pow(10,{0}))`'.format(decimals, parmpath))
                else:
                    msg.append('`chs("{0}")`'.format(parmpath))

            fmsg = " ".join(msg)
            corrmsg = parmname + " ({0})".format(parmitem) + ': ' + fmsg

            if type == "text_meta":
                if currtextmsg == "":
                    finalmsg = corrmsg
                else:
                    finalmsg = currtextmsg + "\n" + corrmsg
            else:
                if parmnode in currtextmsg:
                    corrected = currtextmsg.split(parmnode)
                    corrected.insert(1, parmnode)
                    corrected.insert(2, "\n" + corrmsg)

                    finalmsg = "".join(corrected)
                else:
                    finalmsg = currtextmsg + "\n\n" + parmnode + "\n" + corrmsg

        textmsg.set(finalmsg)

def addMultiParms():
    import hou
    parms = hou.ui.selectParmTuple()
    main_node = hou.pwd()

    for parm in parms:
        parmtuple = hou.parmTuple(parm)
        parmnode = ".:" + parmtuple[0].node().name() + ":."
        parmname = parmtuple[0].description()

        if len(parmtuple)==1:
            parmpath = parmtuple[0].path()
            parmitem = parmtuple[0].name()
        else:
            parmitem = parmtuple[0].name()[:-1]

        try:
            parmnode = ".:" + parmtuple[0].node().name() + ":."
        except:
            hou.ui.displayMessage("Seems like there's a spacer selected. Make sure you avoid that parameter.")

        if len(parmtuple)==1:
            textmsg = main_node.parm("text_info")
            currtextmsg = textmsg.rawValue()

            checkparm = parmtuple[0].eval()
            decimals ='ch("decimals")'
            if isinstance(checkparm, float):
                parmit = parmname + " ({0})".format(parmitem) + ': ' + '`ftrim(round(chs("{1}")*pow(10,{0}))/pow(10,{0}))`'.format(decimals, parmpath)
            else:
                parmit = parmname + " ({0})".format(parmitem) + ': ' + '`chs("{0}")`'.format(parmpath)

            if parmnode in currtextmsg:
                corrected = currtextmsg.split(parmnode)
                corrected.insert(1, parmnode)
                corrected.insert(2, "\n" + parmit)

                finalmsg = "".join(corrected)
            else:
                finalmsg = currtextmsg + "\n\n" + parmnode + "\n" + parmit
        else:
            textmsg = main_node.parm("text_info")
            currtextmsg = textmsg.rawValue()
            msg = []

            for p in parmtuple:
                checkparm = p.eval()
                parmpath = p.path()
                decimals ='ch("decimals")'
                if isinstance(checkparm, float):
                    msg.append('`ftrim(round(chs("{1}")*pow(10,{0}))/pow(10,{0}))`'.format(decimals, parmpath))
                else:
                    msg.append('`chs("{0}")`'.format(parmpath))

            fmsg = " ".join(msg)
            corrmsg = parmname + " ({0})".format(parmitem) + ': ' + fmsg

            if parmnode in currtextmsg:
                corrected = currtextmsg.split(parmnode)
                corrected.insert(1, parmnode)
                corrected.insert(2, "\n" + corrmsg)

                finalmsg = "".join(corrected)
            else:
                finalmsg = currtextmsg + "\n\n" + parmnode + "\n" + corrmsg

        textmsg.set(finalmsg)


def cleanText():
    import hou
    main_node = hou.pwd()
    textparm = main_node.parm("text_info")
    textparm.set("")
    textparm = main_node.parm("text_important")
    textparm.set("")


def addMetadata():
    import hou
    out = hou.node("/out")
    currnode = hou.pwd()
    parm = "vm_image_comment"

    node = [c.name() for c in out.children() if c.type().name() == "ifd"]

    if len(node)==0:
        hou.ui.displayMessage("Seems like you don't have any Mantra nodes.")

    elif len(node)==1:
        nodesel = node[0]
        rop = out.node(nodesel).parm(parm)
        txtrop = rop.rawValue()
        meta = "`chs('/obj/{0}/text_meta')`".format(currnode.name())
 

        if meta in txtrop:
            hou.ui.displayMessage("Links were created successfully.")
            exit()
        else:
            msg = txtrop + '\n' + meta

        rop.set(msg)
        hou.ui.displayMessage("Links were created successfully.")

    else:
        try:
            sel = hou.ui.selectFromList(node, height=1)
            nodesel = node[sel[0]]
        except:
            exit()

        rop = out.node(nodesel).parm(parm)
        txtrop = rop.rawValue()
        meta = "`chs('/obj/{0}/text_meta')`".format(currnode.name())

        if meta in txtrop:
            hou.ui.displayMessage("Links were created successfully.")
            exit()
        else:
            msg = txtrop + '\n' + meta

        rop.set(msg)
        hou.ui.displayMessage("Links were created successfully.")
        

def cleanMetadata():
    import hou
    out = hou.node("/out")
    currnode = hou.pwd()
    parm = "vm_image_comment"

    node = [c.name() for c in out.children() if c.type().name() == "ifd"]

    if len(node)==0:
        hou.ui.displayMessage("Seems like you don't have any Mantra nodes.")

    elif len(node)==1:
        nodesel = node[0]
        rop = out.node(nodesel).parm(parm)

        rop.set("")
        hou.ui.displayMessage("Cleaned up successfully.")

    else:
        try:
            sel = hou.ui.selectFromList(node, height=1)
            nodesel = node[sel[0]]
        except:
            exit()

        rop = out.node(nodesel).parm(parm)
        txtrop = rop.rawValue()


        rop.set("")
        hou.ui.displayMessage("Cleaned up successfully.")
