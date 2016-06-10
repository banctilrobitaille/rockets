from model.Analytics import CommunicationAnalytics
from datetime import datetime
from controller.LogController import LogController
from model.Report import TelemetryAnalyticReport, FlightReport
from controller.FlightController import FlightController


class FlightReportGenerator(object):
    REPORT_BASE_PATH = "./Reports/Flight_Reports/"

    def __init__(self):
        super(FlightReportGenerator, self).__init__()

    @staticmethod
    def generateFlightReport():
        apogeeLine = ChartJSUtil.createLineChart([0],
                                                 "Altitude",
                                                 [0],
                                                 "altitude")

        accelerationLine = ChartJSUtil.createLineChart([0],
                                                       "Acceleration",
                                                       [0],
                                                       "acceleration")

        speedLine = ChartJSUtil.createLineChart([0],
                                                "Speed",
                                                [0],
                                                "speed")

        temperatureLine = ChartJSUtil.createLineChart([0],
                                                      "Temperature",
                                                      [0],
                                                      "temperature")

        report = FlightReport() \
            .withTitle("Flight Report") \
            .withRocketName(FlightController.getInstance().flightModel.rocket.name) \
            .withApogee(FlightController.getInstance().flightModel.apogee) \
            .withMaximumSpeed(FlightController.getInstance().flightModel.maxSpeed) \
            .withCharts("".join([apogeeLine, accelerationLine, speedLine, temperatureLine])) \
            .build()
        FlightReportGenerator.createReportFile(report)

    @staticmethod
    def createReportFile(report):
        reportPath = FlightReportGenerator.REPORT_BASE_PATH + str(datetime.now())
        f = open(reportPath, 'w')
        f.write(report)
        f.close()
        LogController.getInstance().infos("Flight report now available!")


class CommunicationAnalyticsReportGenerator(object):
    REPORT_BASE_PATH = "./Reports/Analytics_Reports/"

    def __init__(self):
        self.__communicationAnalyticModel = CommunicationAnalytics.getInstance()

    @staticmethod
    def generateTelemetryAnalyticReport():
        frameLostPourcentage = str(CommunicationAnalytics.getInstance().nbOfFrameLost /
                                   CommunicationAnalytics.getInstance().nbOfFrameSent * 100)
        nbOfFrameSent = str(CommunicationAnalytics.getInstance().nbOfFrameSent)
        retryAverage = str(CommunicationAnalytics.getInstance().averageNbOfRetries)
        retryTimeHistory = map(lambda time: str(time), CommunicationAnalytics.getInstance().retryHistory['Time'])
        retryNbHistory = map(lambda number: str(number), CommunicationAnalytics.getInstance().retryHistory['Retry'])
        commandSentString = list(CommunicationAnalytics.getInstance().commandSentDict.keys())
        commandSentNumber = list(CommunicationAnalytics.getInstance().commandSentDict.values())

        sentReceivedFrameRatioPie = ChartJSUtil.createPieChart(["Received Frame", "Sent Frame"],
                                                               [CommunicationAnalytics.getInstance().nbOfFrameReceived,
                                                                CommunicationAnalytics.getInstance().nbOfFrameSent],
                                                               "sentReceivedFrame")

        commandStreamerBar = ChartJSUtil.createBarChart(commandSentString,
                                                        "STREAMER STARTED",
                                                        commandSentNumber,
                                                        "commandSent")

        goodBadSentFrameRatioPie = ChartJSUtil.createPieChart(["Good Frame", "Bad Frame"],
                                                              [CommunicationAnalytics.getInstance().nbOfFrameSent -
                                                               CommunicationAnalytics.getInstance().nbOfFrameLost,
                                                               CommunicationAnalytics.getInstance().nbOfFrameLost],
                                                              "sentFrameQA")

        goodBadReceivedFrameRatioPie = ChartJSUtil.createPieChart(["Good Frame", "Bad Frame"],
                                                                  [
                                                                      CommunicationAnalytics.getInstance().nbOfFrameReceived -
                                                                      CommunicationAnalytics.getInstance().nbOfBadFrameReceived,
                                                                      CommunicationAnalytics.getInstance().nbOfBadFrameReceived],
                                                                  "receivedFrameQA")

        retriesHistoryLine = ChartJSUtil.createLineChart(retryTimeHistory,
                                                         "Number of retries",
                                                         retryNbHistory,
                                                         "retryHistory")

        report = TelemetryAnalyticReport() \
            .withTitle("Telemetry Analytics") \
            .withFrameLostPourcentage(frameLostPourcentage) \
            .withNbOfFrameSent(nbOfFrameSent) \
            .withRetryAverage(retryAverage) \
            .withCharts("".join([sentReceivedFrameRatioPie,
                                 commandStreamerBar,
                                 goodBadSentFrameRatioPie,
                                 goodBadReceivedFrameRatioPie,
                                 retriesHistoryLine])) \
            .build()

        CommunicationAnalyticsReportGenerator.createReportFile(report)

    @staticmethod
    def createReportFile(report):
        reportPath = CommunicationAnalyticsReportGenerator.REPORT_BASE_PATH + str(datetime.now())
        f = open(reportPath, 'w')
        f.write(report)
        f.close()
        LogController.getInstance().infos("Analytics report now available!")


class ChartJSUtil(object):
    COLOR = ['''"#FFCE56"''', '''"#36A2EB"''', '''"#FF6384"''']
    HOVER_COLOR = ['''"#FFCE56"''', '''"#36A2EB"''', '''"#FF6384"''']

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
