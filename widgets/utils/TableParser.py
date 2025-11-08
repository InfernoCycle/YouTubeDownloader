import re

class ParseTable:
  def __init__(self):
    self.mainList = []
    
  def strip_ansi(self, text: str) -> str:
    """Remove ANSI escape sequences and other control characters."""
    # Handle both string and bytes
    if isinstance(text, bytes):
        text = text.decode('utf-8', errors='ignore')
    
    # Remove ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    text = ansi_escape.sub('', text)
    
    # Remove other common control characters but keep newlines
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    return text

  def parseHeader(self, string):
    record = {"id":{},"ext":{},"res":{},"fps":{},"FileSize":{},"tbr":{},"proto":{},"vcodec":{},"vbr":{},"acodec":{},"info":{}}
    
    id = re.search("ID(\s+)?", string)
    ext = re.search("EXT(\s+)?", string)
    res = re.search("RESOLUTION(\s+)?", string)
    fps = re.search("FPS(\s+)?", string)
    FileSize = re.search("(\s+)?FILESIZE(\s+)?TBR(\s+)?", string)
    tbr = re.search("(\s+)?\d+k(\s+)?", FileSize.group()) #needs extra handling for empty
    proto = re.search("PROTO(\s+)?", string)
    vcodec = re.search("(\s+)?VCODEC(\s+)?VBR(\s+)?", string)
    vbr = re.search("(\s+)?\d+k(\s+)?", vcodec.group()) #needs extra handling for empty
    acodec = re.search("ACODEC(\s+)?", string)
    info = re.search("MORE INFO(\s+)?", string)
    
    record["id"]["range"] = (id.span()[0], id.span()[1]-1)
    record["ext"]["range"] = (ext.span()[0], ext.span()[1]-1)
    record["res"]["range"] = (res.span()[0], res.span()[1]-1)
    record["fps"]["range"] = (fps.span()[0], fps.span()[1]-1)
    record["FileSize"]["range"] = (FileSize.span()[0], FileSize.span()[1]-1)
    
    record["proto"]["range"] = (proto.span()[0], proto.span()[1]-1)
    record["vcodec"]["range"] = (vcodec.span()[0], vcodec.span()[1]-1)
      
    record["acodec"]["range"] = (acodec.span()[0], acodec.span()[1]-1)
    record["info"]["range"] = (info.span()[0], info.span()[1]-1)
    
    return record

  def table_lines(self, str:str):
    lines = str.split("\n")
    newLines = []
    for i in lines:
      newLines.append(self.strip_ansi(i))
    lines = None
    return newLines
  
  def getInformation(self, txt):
    lines = self.table_lines(txt)
    header_line = lines[0]
    ranges = self.parseHeader(header_line)
    
    video_formats = []
    
    column_names = ["id", "ext", "res", "fps", "FileSize", "tbr", "proto", "vcodec", "vbr", "acodec", "info"]
    for i in range(2, len(lines)):
      id = lines[i][ranges[column_names[0]]["range"][0]:ranges[column_names[0]]["range"][1]].strip()
      ext = lines[i][ranges[column_names[1]]["range"][0]:ranges[column_names[1]]["range"][1]].strip()
      res = lines[i][ranges[column_names[2]]["range"][0]:ranges[column_names[2]]["range"][1]].strip()
      fps = lines[i][ranges[column_names[3]]["range"][0]:ranges[column_names[3]]["range"][1]].strip()
      fs = lines[i][ranges[column_names[4]]["range"][0]:ranges[column_names[4]]["range"][1]].strip()
      fs_cleared = re.sub("(\s+)?\d+k(\s+)?", "", fs)
      tbr = re.search("(\s+)?\d+k(\s+)?", fs)
      if(tbr != None):
        tbr = tbr.group().strip()
      else:
        tbr = "None"
      proto = lines[i][ranges[column_names[6]]["range"][0]:ranges[column_names[6]]["range"][1]].strip()
      vcodec = lines[i][ranges[column_names[7]]["range"][0]:ranges[column_names[7]]["range"][1]].strip()
      vcodec_cleared = re.sub("(\s+)?\d+k(\s+)?", "", vcodec)
      vbr = re.search("(\s+)?\d+k(\s+)?", vcodec)
      if(vbr != None):
        vbr = vbr.group().strip()
      else:
        vbr = "None"
      acodec = lines[i][ranges[column_names[9]]["range"][0]:ranges[column_names[9]]["range"][1]].strip()
      info = lines[i][ranges[column_names[10]]["range"][0]:].strip()
      video_formats.append({"id":id,"ext":ext,"res":res,"fps":fps,"FileSize":fs_cleared,"tbr":tbr,"proto":proto,"vcodec":vcodec_cleared,"vbr":vbr,"acodec":acodec,"info":info})
  
    self.mainList.append(video_formats)
  
  def clearList(self):
    self.mainList.clear()