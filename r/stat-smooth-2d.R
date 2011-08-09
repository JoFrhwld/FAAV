StatSmooth2d <- proto(Stat, {
  calculate_groups <- function(., data, scales, ...) {
    rows.x <- daply(data, .(group), function(df) length(unique(df$x)))
    rows.y <- daply(data, .(group), function(df) length(unique(df$y)))
    
    if (all(rows.x == 1) && length(rows.x) > 1) {
      message("geom_smooth: Only one unique x value each group.", 
        "Maybe you want aes(group = 1)?")
      return(data.frame())
    }
    if (all(rows.y == 1) && length(rows.y) > 1) {
      message("geom_smooth: Only one unique y value each group.", 
        "Maybe you want aes(group = 1)?")
      return(data.frame())
    }
    
    .super$calculate_groups(., data, scales, ...)
  }
  
  calculate <- function(., data, scales, 
                        method="auto", formula.y = y~z,
                                       formula.x = x~z,
                        n=80,
                        zseq = NULL, level=0.95, 
                        na.rm = FALSE, ...) {
    data <- remove_missing(data, na.rm, c("x", "y", "z"), name="stat_smooth2d")
    if (length(unique(data$x)) < 2 | length(unique(data$y)) < 2) {
      # Not enough data to perform fit
      return(data.frame())
    }
    
    # Figure out what type of smoothing to do: loess for small datasets,
    # gam with a cubic regression basis for large data
    if (is.character(method) && method == "auto") {
      if (nrow(data) < 1000) {
        method <- "loess"
      } else {
        try_require("mgcv")
        method <- gam
        formula.y <- y ~ s(z, bs = "cs")
        formula.x <- x ~ s(z, bs = "cs")
      }
    }
    
    if (is.null(data$weight)) data$weight <- 1
    
    if (is.null(zseq)) {
      if (is.integer(data$z)) {
        zseq <- sort(unique(data$z))
      } else {
        range <- range(data$z, na.rm=TRUE)   
        zseq <- seq(range[1], range[2], length=n)
      } 
    }
    
    if (is.character(method)) method <- match.fun(method)
    
    method.special.y <- function(...){ 
      method(formula.y, data=data, weights=weight, ...)
    }
    method.special.x <- function(...){
      method(formula.x, data=data, weights=weight, ...)
    }
    model.y <- safe.call(method.special.y, list(...), names(formals(method)))
    model.x <- safe.call(method.special.x, list(...), names(formals(method)))
    
    pred.y <- stats::predict(model.y, newdata = data.frame(z = zseq))
    pred.x <- stats::predict(model.x, newdata = data.frame(z = zseq))
    
    df <- data.frame(x = as.vector(pred.x), y = as.vector(pred.y), z = zseq)
    df <- arrange(df, z)
    return(df)
  }
  
  objname <- "smooth2d" 
  desc <- "Add a 2d smoother"
  details <- "Aids the eye in seeing patterns in the presence of overplotting."
  icon <- function(.) GeomPath$icon()
  
  required_aes <- c("x", "y", "z")
  default_geom <- function(.) GeomPath
  desc_params <- list(
    method = "smoothing method (function) to use, eg. lm, glm, gam, loess, rlm",
    formula =  "formula to use in smoothing function, eg. y ~ x, y ~ poly(x, 2), y ~ log(x)",
    se = "display confidence interval around smooth? (true by default, see level to control)",
    fullrange = "should the fit span the full range of the plot, or just the data",
    level = "level of confidence interval to use (0.95 by default)",
    n = "number of points to evaluate smoother at",
    xseq = "exact points to evaluate smooth at, overrides n",
    "..." = "other arguments are passed to smoothing function"
  )
  desc_outputs <- list(
    "y" = "predicted value",
    "ymin" = "lower pointwise confidence interval around the mean",
    "ymax" = "upper pointwise confidence interval around the mean",
    "se" = "standard error"
  )
  
  seealso <- list(
    lm = "for linear smooths",
    glm = "for generalised linear smooths",
    loess = "for local smooths"
  )
  
#   examples <- function(.) {
#     c <- ggplot(mtcars, aes(qsec, wt))
#     c + stat_smooth() 
#     c + stat_smooth() + geom_point()
# 
#     # Adjust parameters
#     c + stat_smooth(se = FALSE) + geom_point()
# 
#     c + stat_smooth(span = 0.9) + geom_point()  
#     c + stat_smooth(method = "lm") + geom_point() 
#     
#     library(splines)
#     c + stat_smooth(method = "lm", formula = y ~ ns(x,3)) +
#       geom_point()  
#     c + stat_smooth(method = MASS::rlm, formula= y ~ ns(x,3)) + geom_point()  
#     
#     # The default confidence band uses a transparent colour. 
#     # This currently only works on a limited number of graphics devices 
#     # (including Quartz, PDF, and Cairo) so you may need to set the
#     # fill colour to a opaque colour, as shown below
#     c + stat_smooth(fill = "grey50", size = 2, alpha = 1)
#     c + stat_smooth(fill = "blue", size = 2, alpha = 1)
#     
#     # The colour of the line can be controlled with the colour aesthetic
#     c + stat_smooth(fill="blue", colour="darkblue", size=2)
#     c + stat_smooth(fill="blue", colour="darkblue", size=2, alpha = 0.2)
#     c + geom_point() + 
#       stat_smooth(fill="blue", colour="darkblue", size=2, alpha = 0.2)
#     
#     # Smoothers for subsets
#     c <- ggplot(mtcars, aes(y=wt, x=mpg)) + facet_grid(. ~ cyl)
#     c + stat_smooth(method=lm) + geom_point() 
#     c + stat_smooth(method=lm, fullrange=T) + geom_point() 
#     
#     # Geoms and stats are automatically split by aesthetics that are factors
#     c <- ggplot(mtcars, aes(y=wt, x=mpg, colour=factor(cyl)))
#     c + stat_smooth(method=lm) + geom_point() 
#     c + stat_smooth(method=lm, aes(fill = factor(cyl))) + geom_point() 
#     c + stat_smooth(method=lm, fullrange=TRUE, alpha = 0.1) + geom_point() 
# 
#     # Use qplot instead
#     qplot(qsec, wt, data=mtcars, geom=c("smooth", "point"))
#     
#     # Example with logistic regression
#     data("kyphosis", package="rpart")
#     qplot(Age, Kyphosis, data=kyphosis)
#     qplot(Age, data=kyphosis, facets = . ~ Kyphosis, binwidth = 10)
#     qplot(Age, Kyphosis, data=kyphosis, position="jitter")
#     qplot(Age, Kyphosis, data=kyphosis, position=position_jitter(height=0.1))
# 
#     qplot(Age, as.numeric(Kyphosis) - 1, data = kyphosis) +
#       stat_smooth(method="glm", family="binomial")
#     qplot(Age, as.numeric(Kyphosis) - 1, data=kyphosis) +
#       stat_smooth(method="glm", family="binomial", formula = y ~ ns(x, 2))
#     
#   }
})

stat_smooth2d <- StatSmooth2d$build_accessor()m