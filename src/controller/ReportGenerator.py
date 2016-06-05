from model.Analytics import CommunicationAnalytics
from datetime import datetime


class CommunicationAnalyticsReportGenerator(object):
    REPORT_BASE_PATH = "./Reports/Analytics_Reports/Communication/"
    REPORT_RESOURCES_PATH = "../../../Report_Resources/"
    JQUERY_PATH = "jquery/jquery-2.2.4.min.js"
    CHART_JS_PATH = "chartJS/Chart.min.js"
    BOOTSTRAP_CSS_PATH = "bootstrap/css/bootstrap.min.css"
    BOOTSTRAP_JS_PATH = "bootstrap/js/bootstrap.min.js"
    BOOTSTRAP_CSS_INCLUDE = '''<link href="{}" rel="stylesheet">'''.format(REPORT_RESOURCES_PATH + BOOTSTRAP_CSS_PATH)
    BOOTSTRAP_JS_INCLUDE = '''<script src="{}"></script>'''.format(REPORT_RESOURCES_PATH + BOOTSTRAP_JS_PATH)
    JQUERY_INCLUDE = '''<script src="{}"></script>'''.format(REPORT_RESOURCES_PATH + JQUERY_PATH)
    CHART_JS_INCLUDE = '''<script src="{}"></script>'''.format(REPORT_RESOURCES_PATH + CHART_JS_PATH)

    def __init__(self):
        self.__communicationAnalyticModel = CommunicationAnalytics.getInstance()
        self.__reportContent = None

    def generateReportContent(self):

        self.__reportContent = \
            '''<!DOCTYPE html>
                <html lang="en">
                    <head>
                        <meta charset="utf-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <center><title>Communication Analytics</title></center>
                        <!-- Bootstrap -->
                        {}
                    </head>
                    <body>
                        <div class="container">
                            <div class="jumbotron">
                                <h1>Communication Analytics</h1>
                            </div>
                            <div class="row">
                                <div class="col-sm-6">
                                  <h2 class="text-center">SENT AND RECEIVED FRAME</h2>
                                  <canvas id="sentReceivedFrame"></canvas>
                                </div>
                                 <div class="col-sm-6">
                                  <h2 class="text-center">COMMAND SENT</h2>
                                  <canvas id="commandSent"></canvas>
                                </div>
                            </div>
                        </div>

                        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
                        {}
                        <!-- Include all compiled plugins (below), or include individual files as needed -->
                        {}
                        <!-- Include chart  JS -->
                        {}'''.format(self.BOOTSTRAP_CSS_INCLUDE, self.JQUERY_INCLUDE, self.BOOTSTRAP_JS_INCLUDE,
                                  self.CHART_JS_INCLUDE) + \
                        ChartJSUtil.createPieChart(["Received Frame", "Sent Frame"],
                                                   [CommunicationAnalytics.getInstance().nbOfFrameReceived,
                                                    CommunicationAnalytics.getInstance().nbOfFrameSent],
                                                   "sentReceivedFrame") + \
                        ChartJSUtil.createPieChart(['''"Rocket Discovery"'''],
                                                   [15],
                                                   "commandSent") + \
                        '''
                    </body>
                </html>'''

    def createReportFile(self):
        f = open(self.REPORT_BASE_PATH + str(datetime.now()), 'w')
        f.write(self.__reportContent)
        f.close()


class ChartJSUtil(object):

    COLOR = ['''"#FFCE56"''', '''"#36A2EB"''', '''"#FF6384"''']
    HOVER_COLOR = ['''"#FFCE56"''' , '''"#36A2EB"''', '''"#FF6384"''']

    @staticmethod
    def createPieChart(labels, data, canvasId):

        data = ChartJSUtil.createPieChartData(labels, data)
        context = '''var ctx = document.getElementById("{}").getContext("2d");'''.format(canvasId)
        pieChart = '''var myPieChart = new Chart(ctx,{type: 'pie',data: data,});'''
        return "\n".join(["<script>", data, context, pieChart, "</script>"])


    @staticmethod
    def createBarChart(barLabels, title, data, canvasId):
        pass

    @staticmethod
    def createPieChartData(labels, data):

        labels = '''labels: [{}],'''.format(reduce(lambda x, y: "".join(['''"''', x, '''"''', ",", '''"''', y,
                                                                        '''"''']), labels))

        data = "data: [{}],".format(reduce(lambda x, y: "".join([str(x), ",", str(y)]), data))

        backgroundColor = "".join(["backgroundColor: [", reduce(lambda x, y: "".join([x, ",", y]),
                                                                ChartJSUtil.COLOR[0:len(data)]), "],"])

        hoverBackgroundColor = "".join(["hoverBackgroundColor: [", reduce(lambda x, y: "".join([x, ",", y]),
                                                                          ChartJSUtil.HOVER_COLOR[0:len(data)]), "]"])

        dataset = "".join(["datasets: [{", data, backgroundColor, hoverBackgroundColor, "}]"])

        return "".join(["var data ={", labels, dataset, "};"])


    @staticmethod
    def createBarChartData(barLabels, title, data):
        pass