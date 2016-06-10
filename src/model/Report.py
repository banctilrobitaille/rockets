class Report(object):

    REPORT_BASE_PATH = "./Reports/Analytics_Reports/Communication/"
    REPORT_RESOURCES_PATH = "../../Report_Resources/"
    JQUERY_PATH = "jquery/jquery-2.2.4.min.js"
    CHART_JS_PATH = "chartJS/Chart.min.js"
    BOOTSTRAP_CSS_PATH = "bootstrap/css/bootstrap.min.css"
    BOOTSTRAP_JS_PATH = "bootstrap/js/bootstrap.min.js"
    BOOTSTRAP_CSS_INCLUDE = '''<link href="{}" rel="stylesheet">'''.format(REPORT_RESOURCES_PATH + BOOTSTRAP_CSS_PATH)
    BOOTSTRAP_JS_INCLUDE = '''<script src="{}"></script>'''.format(REPORT_RESOURCES_PATH + BOOTSTRAP_JS_PATH)
    JQUERY_INCLUDE = '''<script src="{}"></script>'''.format(REPORT_RESOURCES_PATH + JQUERY_PATH)
    CHART_JS_INCLUDE = '''<script src="{}"></script>'''.format(REPORT_RESOURCES_PATH + CHART_JS_PATH)

    def __init__(self):
        pass


class TelemetryAnalyticReport(Report):

    LOGO = "Images/rocketsAnalytics.png"

    def __init__(self):
        super(TelemetryAnalyticReport, self).__init__()
        self.__title = ""
        self.__frameLostPourcentage = ""
        self.__nbOfFrameSent = ""
        self.__retryAverage = ""
        self.__charts = ""
        self.__content = '''<!DOCTYPE html>
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
                                        src="{}">
                                    </div>
                                    <div class="col-md-10">
                                        <h1>{}</h1>
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
                                                        <hr>
                                                        <h4><strong>LOSS %:</strong> {}%</h4>
                                                        <hr>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h4><strong>NB OF FRAME SENT:</strong> {}</h4>
                                                        <hr>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h4><strong>RETRIES/STREAMER:</strong> {}</h4>
                                                        <hr>
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
                        {}
                        <!-- Chart -->
                        {}
                        </body>
                </html>'''

    def withTitle(self, title):
        self.__title = title
        return self

    def withFrameLostPourcentage(self, frameLostPourcentage):
        self.__frameLostPourcentage = frameLostPourcentage
        return self

    def withNbOfFrameSent(self, nbOfFrameSent):
        self.__nbOfFrameSent = nbOfFrameSent
        return self

    def withRetryAverage(self, retryAverage):
        self.__retryAverage = retryAverage
        return self

    def withCharts(self, charts):
        self.__charts = charts
        return self

    def build(self):
        return self.__content.format(self.BOOTSTRAP_CSS_INCLUDE, "".join([self.REPORT_RESOURCES_PATH, self.LOGO]),
                                     self.__title, self.__frameLostPourcentage, self.__nbOfFrameSent,
                                     self.__retryAverage, self.JQUERY_INCLUDE, self.BOOTSTRAP_JS_INCLUDE,
                                     self.CHART_JS_INCLUDE, self.__charts)


class FlightReport(Report):

    LOGO = "Images/rocketsFlight.png"

    def __init__(self):
        super(FlightReport, self).__init__()
        self.__title = ""
        self.__rocketName = ""
        self.__apogee = ""
        self.__maximumSpeed = ""
        self.__charts = ""
        self.__content =\
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
                                        src="{}">
                                    </div>
                                    <div class="col-md-10">
                                        <h1>{}</h1>
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
                                                        <hr>
                                                        <h4><strong>ROCKET NAME:</strong> {}</h4>
                                                        <hr>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h4><strong>CONNECTION TIME:</strong> </h4>
                                                        <hr>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h4><strong>APOGEE:</strong> {} FEET</h4>
                                                        <hr>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h4><strong>TIME TO APOGEE:</strong>  SEC</h4>
                                                        <hr>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h4><strong>MAXIMUM SPEED:</strong> {} MPH</h4>
                                                        <hr>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h4><strong>MAXIMUM ACCEL:</strong>  M/S2</h4>
                                                        <hr>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h4><strong>MAXIMUM TEMPERATURE:</strong>  C</h4>
                                                        <hr>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <h4><strong>MINIMUM TEMPERATURE:</strong>  C</h4>
                                                        <hr>
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
                                            <div class="panel-heading">FLIGHT</div>
                                            <div class="panel-body">
                                                <div class="row">
                                                    <div class="col-md-6">
                                                      <h2 class="text-center">ALTITUDE</h2>
                                                      <canvas id="altitude"></canvas>
                                                    </div>
                                                     <div class="col-md-6">
                                                      <h2 class="text-center">ACCELERATION</h2>
                                                      <canvas id="acceleration"></canvas>
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-md-6">
                                                      <h2 class="text-center">SPEED</h2>
                                                      <canvas id="speed"></canvas>
                                                    </div>
                                                     <div class="col-md-6">
                                                      <h2 class="text-center">TEMPERATURE</h2>
                                                      <canvas id="temperature"></canvas>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="panel panel-default">
                                            <div class="panel-heading">TELEMETRY</div>
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
                        {}
                        <!-- Charts -->
                        {}
                    </body>
                </html>'''

    def withTitle(self, title):
        self.__title = title
        return self

    def withRocketName(self, rocketName):
        self.__rocketName = rocketName
        return self

    def withApogee(self, apogee):
        self.__apogee = apogee
        return self

    def withMaximumSpeed(self, maximumSpeed):
        self.__maximumSpeed = maximumSpeed
        return self

    def withCharts(self, charts):
        self.__charts = charts
        return self

    def build(self):
        return self.__content.format(self.BOOTSTRAP_CSS_INCLUDE, "".join([self.REPORT_RESOURCES_PATH, self.LOGO]),
                                     self.__title, self.__rocketName, self.__apogee,
                                     self.__maximumSpeed, self.JQUERY_INCLUDE, self.BOOTSTRAP_JS_INCLUDE,
                                     self.CHART_JS_INCLUDE, self.__charts)
