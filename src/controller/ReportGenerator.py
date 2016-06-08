from model.Analytics import CommunicationAnalytics
from datetime import datetime
from controller.LogController import LogController


class ReportGenerator(object):
    REPORT_RESOURCES_PATH = "../../Report_Resources/"
    JQUERY_PATH = "jquery/jquery-2.2.4.min.js"
    CHART_JS_PATH = "chartJS/Chart.min.js"
    BOOTSTRAP_CSS_PATH = "bootstrap/css/bootstrap.min.css"
    BOOTSTRAP_JS_PATH = "bootstrap/js/bootstrap.min.js"
    BOOTSTRAP_CSS_INCLUDE = '''<link href="{}" rel="stylesheet">'''.format(REPORT_RESOURCES_PATH + BOOTSTRAP_CSS_PATH)
    BOOTSTRAP_JS_INCLUDE = '''<script src="{}"></script>'''.format(REPORT_RESOURCES_PATH + BOOTSTRAP_JS_PATH)
    JQUERY_INCLUDE = '''<script src="{}"></script>'''.format(REPORT_RESOURCES_PATH + JQUERY_PATH)
    CHART_JS_INCLUDE = '''<script src="{}"></script>'''.format(REPORT_RESOURCES_PATH + CHART_JS_PATH)


class FlightReportGenerator(ReportGenerator):

    REPORT_BASE_PATH = "./Reports/Flight_Reports/"

    def __init__(self):
        super(FlightReportGenerator, self).__init__()
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
                                <div class="row">
                                    <div class="col-md-2">
                                        <img alt=" " style="max-width: 100%; max-height: 100%;"
                                        src="../../Report_Resources/Images/rocketsFlight.png">
                                    </div>
                                    <div class="col-md-10">
                                        <h1>Flight Report</h1>
                                    </div>
                                </div>
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
                                                        <h3>{}</h3>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h3>{}</h3>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h3>{}</h3>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="col-md-1"></div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-8">
                                    <div class="row">
                                        <div class="panel panel-default">
                                            <div class="panel-heading">USAGE</div>
                                            <div class="panel-body">

                                            </div>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="panel panel-default">
                                            <div class="panel-heading">QUALITY OF SERVICE</div>
                                            <div class="panel-body">

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
                        {}'''.format(self.BOOTSTRAP_CSS_INCLUDE,"" , "" , "",
                                            self.JQUERY_INCLUDE, self.BOOTSTRAP_JS_INCLUDE, self.CHART_JS_INCLUDE) + \
                        '''
                    </body>
                </html>'''

    def createReportFile(self):
            reportPath = self.REPORT_BASE_PATH + str(datetime.now())
            f = open(reportPath, 'w')
            f.write(self.__reportContent)
            f.close()
            LogController.getInstance().infos("Flight report now available!")


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

        frameLostPourcentage = str(CommunicationAnalytics.getInstance().nbOfFrameLost /
                                   CommunicationAnalytics.getInstance().nbOfFrameSent * 100)
        nbOfFrameSent = str(CommunicationAnalytics.getInstance().nbOfFrameSent)
        retryAverage = str(CommunicationAnalytics.getInstance().averageNbOfRetries)
        retryTimeHistory = map(lambda time: str(time), CommunicationAnalytics.getInstance().retryHistory['Time'])
        retryNbHistory = map(lambda number: str(number), CommunicationAnalytics.getInstance().retryHistory['Retry'])
        commandSentString = list(CommunicationAnalytics.getInstance().commandSentDict.keys())
        commandSentNumber = list(CommunicationAnalytics.getInstance().commandSentDict.values())

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
                                <div class="row">
                                    <div class="col-md-2">
                                        <img alt=" " style="max-width: 100%; max-height: 100%;"
                                        src="../../../Report_Resources/Images/rocketsAnalytics.png">
                                    </div>
                                    <div class="col-md-10">
                                        <h1>Telemetry Analytics</h1>
                                    </div>
                                </div>
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
                                                        <h3>LOSS %: {}%</h3>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h3>NB OF FRAME SENT: {}</h3>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h3>RETRIES/STREAMER: {}</h3>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="col-md-1"></div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-8">
                                    <div class="row">
                                        <div class="panel panel-default">
                                            <div class="panel-heading">USAGE</div>
                                            <div class="panel-body">
                                                <div class="col-md-6">
                                                  <h2 class="text-center">SENT AND RECEIVED FRAMES</h2>
                                                  <canvas id="sentReceivedFrame"></canvas>
                                                </div>
                                                 <div class="col-md-6">
                                                  <h2 class="text-center">COMMAND STREAMER</h2>
                                                  <canvas id="commandSent"></canvas>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="panel panel-default">
                                            <div class="panel-heading">QUALITY OF SERVICE</div>
                                            <div class="panel-body">
                                                <div class="row">
                                                    <div class="col-md-6">
                                                      <h2 class="text-center">SENT FRAMES</h2>
                                                      <canvas id="sentFrameQA"></canvas>
                                                    </div>
                                                     <div class="col-md-6">
                                                      <h2 class="text-center">RECEIVED FRAMES</h2>
                                                      <canvas id="receivedFrameQA"></canvas>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <canvas id="retryHistory"></canvas>
                                                    </div>
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
                        {}'''.format(self.BOOTSTRAP_CSS_INCLUDE,frameLostPourcentage , nbOfFrameSent , retryAverage,
                                            self.JQUERY_INCLUDE, self.BOOTSTRAP_JS_INCLUDE, self.CHART_JS_INCLUDE) + \
                        ChartJSUtil.createPieChart(["Received Frame", "Sent Frame"],
                                                   [CommunicationAnalytics.getInstance().nbOfFrameReceived,
                                                    CommunicationAnalytics.getInstance().nbOfFrameSent],
                                                   "sentReceivedFrame") + \
                        ChartJSUtil.createBarChart(commandSentString,
                                                   "STREAMER STARTED",
                                                   commandSentNumber,
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
                        ChartJSUtil.createLineChart(retryTimeHistory,
                                                    "Number of retries",
                                                    retryNbHistory,
                                                    "retryHistory") + \
                        '''
                    </body>
                </html>'''

    def createReportFile(self):
        reportPath = self.REPORT_BASE_PATH + str(datetime.now())
        f = open(reportPath, 'w')
        f.write(self.__reportContent)
        f.close()
        LogController.getInstance().infos("Analytics report now available!")


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
        barChart = '''var myBarChart = new Chart(ctx,{type: 'bar',data: data,});'''
        return "\n".join(["<script>", data, context, barChart, "</script>"])

    @staticmethod
    def createDonutChart(labels, data, canvasId):

        data = ChartJSUtil.createDonutChartData(labels, data)
        context = '''var ctx = document.getElementById("{}").getContext("2d");'''.format(canvasId)
        pieChart = '''var myDonutChart = new Chart(ctx,{type: 'doughnut',data: data,});'''
        return "\n".join(["<script>", data, context, pieChart, "</script>"])

    @staticmethod
    def createLineChart(labels, title, data, canvasId):

        data = ChartJSUtil.createLineChartData(labels, title, data)
        context = '''var ctx = document.getElementById("{}").getContext("2d");'''.format(canvasId)
        pieChart = '''var myLineChart = new Chart(ctx,{type: 'line',data: data,});'''
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

    @staticmethod
    def createLineChartData(lineLabels, title, data):

        lineLabels = '''labels: [{}],'''.format(', '.join('"{0}"'.format(label) for label in lineLabels))

        data = "data: [{}],".format(reduce(lambda x, y: "".join([str(x), ",", str(y)]), data))
        label = "label: {},".format("".join(['''"''', title, '''"''']))
        color = '''fill: false,
                lineTension: 0.1,
                backgroundColor: "rgba(75,192,192,0.4)",
                borderColor: "rgba(75,192,192,1)",
                borderCapStyle: 'butt',
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: 'miter',
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,'''

        datasets = "\n".join(["datasets: [{", label, color, data, "}]"])

        return "\n".join(["var data ={", lineLabels, datasets, "};"])