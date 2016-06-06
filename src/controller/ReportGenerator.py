from model.Analytics import CommunicationAnalytics
from datetime import datetime


class ReportGenerator(object):
    REPORT_RESOURCES_PATH = "../../../Report_Resources/"
    JQUERY_PATH = "jquery/jquery-2.2.4.min.js"
    CHART_JS_PATH = "chartJS/Chart.min.js"
    BOOTSTRAP_CSS_PATH = "bootstrap/css/bootstrap.min.css"
    BOOTSTRAP_JS_PATH = "bootstrap/js/bootstrap.min.js"
    BOOTSTRAP_CSS_INCLUDE = '''<link href="{}" rel="stylesheet">'''.format(REPORT_RESOURCES_PATH + BOOTSTRAP_CSS_PATH)
    BOOTSTRAP_JS_INCLUDE = '''<script src="{}"></script>'''.format(REPORT_RESOURCES_PATH + BOOTSTRAP_JS_PATH)
    JQUERY_INCLUDE = '''<script src="{}"></script>'''.format(REPORT_RESOURCES_PATH + JQUERY_PATH)
    CHART_JS_INCLUDE = '''<script src="{}"></script>'''.format(REPORT_RESOURCES_PATH + CHART_JS_PATH)


class FlightReportGenerator(ReportGenerator):

    def __init__(self):
        super(FlightReportGenerator, self).__init__()


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
                        <div class="container-fluid">
                            <div class="jumbotron">
                                <h1>Telemetry Analytics</h1>
                            </div>
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="panel panel-info">
                                        <div class="panel-heading">QUICK STATS</div>
                                        <div class="row">
                                            <div class="col-md-1"></div>
                                            <div class="col-md-10">
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h3>LOSS %: 100%</h3>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h3>NB OF FRAME SENT: 15</h3>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="col-md-1"></div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-9">
                                    <div class="row">
                                        <div class="panel panel-default">
                                            <div class="panel-heading">USAGE</div>
                                            <div class="panel-body">
                                                <div class="col-md-6">
                                                  <h2 class="text-center">SENT AND RECEIVED FRAMES</h2>
                                                  <canvas id="sentReceivedFrame"></canvas>
                                                </div>
                                                 <div class="col-md-6">
                                                  <h2 class="text-center">COMMANDS SENT</h2>
                                                  <canvas id="commandSent"></canvas>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="panel panel-default">
                                            <div class="panel-heading">QUALITY OF SERVICE</div>
                                            <div class="panel-body">
                                                <div class="col-md-6">
                                                  <h2 class="text-center">QUALITY OF SENT FRAMES</h2>
                                                  <canvas id="sentFrameQA"></canvas>
                                                </div>
                                                 <div class="col-md-6">
                                                  <h2 class="text-center">QUALITY OF RECEIVED FRAMES</h2>
                                                  <canvas id="receivedFrameQA"></canvas>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
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
                        ChartJSUtil.createBarChart(["Rocket Discovery", "Start Camera", "Stop Camera",
                                                    "Start Stream", "Stop Stream"],
                                                   "Command Sent",
                                                   [10, 12, 50, 5, 80],
                                                   "commandSent") + \
                        ChartJSUtil.createPieChart(["Good Frame", "Bad Frame"],
                                                   [CommunicationAnalytics.getInstance().nbOfFrameSent -
                                                    CommunicationAnalytics.getInstance().nbOfFrameLost,
                                                    CommunicationAnalytics.getInstance().nbOfFrameLost],
                                                   "sentFrameQA") + \
                        ChartJSUtil.createPieChart(["Good Frame", "Bad Frame"],
                                                   [CommunicationAnalytics.getInstance().nbOfFrameReceived -
                                                    CommunicationAnalytics.getInstance().nbOfBadFrameReceived,
                                                    CommunicationAnalytics.getInstance().nbOfBadFrameReceived],
                                                   "receivedFrameQA") + \
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

        data = ChartJSUtil.createBarChartData(barLabels, title, data)
        context = '''var ctx = document.getElementById("{}").getContext("2d");'''.format(canvasId)
        barChart = '''var myPieChart = new Chart(ctx,{type: 'bar',data: data,});'''
        return "\n".join(["<script>", data, context, barChart, "</script>"])

    @staticmethod
    def createDonutChart(labels, data, canvasId):

        data = ChartJSUtil.createDonutChartData(labels, data)
        context = '''var ctx = document.getElementById("{}").getContext("2d");'''.format(canvasId)
        pieChart = '''var myPieChart = new Chart(ctx,{type: 'doughnut',data: data,});'''
        return "\n".join(["<script>", data, context, pieChart, "</script>"])

    @staticmethod
    def createPieChartData(labels, data):

        labels = '''labels: [{}],'''.format(', '.join('"{0}"'.format(label) for label in labels))

        data = "data: [{}],".format(reduce(lambda x, y: "".join([str(x), ",", str(y)]), data))

        backgroundColor = "".join(["backgroundColor: [", reduce(lambda x, y: "".join([x, ",", y]),
                                                                ChartJSUtil.COLOR[0:len(data)]), "],"])

        hoverBackgroundColor = "".join(["hoverBackgroundColor: [", reduce(lambda x, y: "".join([x, ",", y]),
                                                                          ChartJSUtil.HOVER_COLOR[0:len(data)]), "]"])

        dataset = "".join(["datasets: [{", data, backgroundColor, hoverBackgroundColor, "}]"])

        return "".join(["var data ={", labels, dataset, "};"])

    @staticmethod
    def createDonutChartData(labels, data):

        labels = '''labels: [{}],'''.format(', '.join('"{0}"'.format(label) for label in labels))

        data = "data: [{}],".format(reduce(lambda x, y: "".join([str(x), ",", str(y)]), data))

        backgroundColor = "".join(["backgroundColor: [", reduce(lambda x, y: "".join([x, ",", y]),
                                                                ChartJSUtil.COLOR[0:len(data)]), "],"])

        hoverBackgroundColor = "".join(["hoverBackgroundColor: [", reduce(lambda x, y: "".join([x, ",", y]),
                                                                          ChartJSUtil.HOVER_COLOR[0:len(data)]), "]"])

        dataset = "".join(["datasets: [{", data, backgroundColor, hoverBackgroundColor, "}]"])

        return "".join(["var data ={", labels, dataset, "};"])

    @staticmethod
    def createBarChartData(barLabels, title, data):

        barLabels = '''labels: [{}],'''.format(', '.join('"{0}"'.format(label) for label in barLabels))

        data = "data: [{}],".format(reduce(lambda x, y: "".join([str(x), ",", str(y)]), data))
        label = "label: {},".format("".join(['''"''', title, '''"''']))
        color = '''backgroundColor: "rgba(255,99,132,0.2)",
                borderColor: "rgba(255,99,132,1)",
                borderWidth: 1,
                hoverBackgroundColor: "rgba(255,99,132,0.4)",
                hoverBorderColor: "rgba(255,99,132,1)",'''

        datasets = "\n".join(["datasets: [{", label, color, data, "}]"])

        return "\n".join(["var data ={", barLabels, datasets, "};"])
